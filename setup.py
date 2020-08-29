#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.

import setuptools

setuptools.setup(
            name="clarabox",
            version="0.0.1",
            author="Christoph Heuel",
            author_email="christoph@heuel-web.de",
            description=("Clarabox is similar to a Phoniebox, but slightly \
                         modified"),
            license="MIT",
            keywords="JukeBox Player",
            package_dir={"": "clarabox/"},
            packages=setuptools.find_packages("clarabox"),
            classifiers=[
                        "Development Status :: 3 - Alpha",
                        "Topic :: Utilities",
                        "License :: OSI Approved :: MIT License",
                    ],
)
