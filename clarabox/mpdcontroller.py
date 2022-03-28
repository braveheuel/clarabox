"""MPD Controller"""
import mpd.asyncio
import datetime
import logging
import yaml


class NoKnownActionException(Exception):
    pass

class CardIDNotKnownException(Exception):
    pass

class MusicController:

    def __init__(self, host, port, rfid_map, reswipe_time, btn_queue):
        self.mpc = mpd.asyncio.MPDClient()
        self.rfid_map = rfid_map
        self.swipe_timeout = datetime.timedelta(seconds=reswipe_time)
        self._swipe_ts = datetime.datetime(2020, 1, 1)
        self.host = host
        self.port = port
        self.btn_queue = btn_queue
        self.last_swiped_id = 0
        self.last_swiped_id_count = 0

        with open(rfid_map, "r") as stream:
            self._yaml = yaml.safe_load(stream)

        logging.debug(self._yaml)

    async def connect_mpd(self):
        """ Connect to MPD Server and start GPIO listen queue
        """
        await self.mpc.connect(self.host, self.port)
        await self._run_listen_btn()

    async def _run_listen_btn(self):
        while True:
            logging.info("Run queue.get")
            cmd = await self.btn_queue.get()
            logging.info("Received Button Event: %s", cmd)
            await self.command(cmd)
            self.btn_queue.task_done()

    async def play_card(self, cardid):
        current_ts = datetime.datetime.now()
        td = current_ts - self._swipe_ts

        if cardid == self.last_swiped_id:
            self.last_swiped_id_count += 1
        else:
            self.last_swiped_id = cardid
            self.last_swiped_id_count = 0

        if self.last_swiped_id_count > 0:
            logging.info("Card already playing, skipping swipe!")
            return

        if td > self.swipe_timeout:
            try:
                (is_command, data) = self.retrieve_card(cardid)
            except CardIDNotKnownException as e:
                logging.warning(e)
                return
            except NoKnownActionException as e:
                logging.warning(e)
                return
            logging.info("Received CardID: %s with data: %s", cardid, data)
            if is_command:
                await self.command(data)
            else:
                await self.play_pl(data)
            self._swipe_ts = current_ts
        else:
            logging.info("Swipe Timeout (%f) not reached: %f",
                         self.swipe_timeout.total_seconds(), td.total_seconds())

    def retrieve_card(self, cardid):
        if cardid in self._yaml:
            if "playlist" in self._yaml[cardid]:
                return (False, self._yaml[cardid]["playlist"])
            elif "command" in self._yaml[cardid]:
                return (True, self._yaml[cardid]["command"])
            else:
                raise NoKnownActionException()
        else:
            raise CardIDNotKnownException("Could not find CardID {0}"
                                          .format(cardid))

    async def command(self, cmd):
        ucmd = cmd.lower()
        if ucmd.startswith("play"):
            await self.play()
        elif ucmd.startswith("sto"):
            await self.stop()
        elif ucmd.startswith("pre"):
            await self.previous()
        elif ucmd.startswith("nex"):
            await self.next()
        elif ucmd.startswith("vol+"):
            await self.volumeup()
        elif ucmd.startswith("vol-"):
            await self.volumedown()

    async def play(self):
        status = await self.mpc.status()
        if status["state"] == "play":
            await self.mpc.pause()
        else:
            await self.mpc.play()

    async def stop(self):
        await self.mpc.stop()

    async def next(self):
        status = await self.mpc.status()
        if not status["state"] == "stop":
            await self.mpc.next()

    async def previous(self):
        status = await self.mpc.status()
        if not status["state"] == "stop":
            await self.mpc.previous()

    async def volumeup(self):
        vol = await self.get_volume() + 1
        if vol > 30:
            vol = 30
        await self.mpc.setvol(vol)

    async def volumedown(self):
        vol = await self.get_volume() - 1
        if vol < 0:
            vol = 0
        await self.mpc.setvol(vol)

    async def get_volume(self):
        status = await self.mpc.status()
        vol = int(status["volume"])
        return vol

    async def play_pl(self, playlist):
        await self.mpc.stop()
        await self.mpc.clear()
        try:
            await self.mpc.load(playlist)
        except mpd.base.CommandError as e:
            logging.warning(e)
            return
        await self.mpc.play()

    async def status(self):
        return await self.mpc.status()
