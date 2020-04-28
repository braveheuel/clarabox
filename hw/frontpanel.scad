// Version: 0.2
// Front Panel for The Clarabox
// inner of the wodden box: 28x13x17cm
size=[139, 129, 4];
// Arcade Button:
//   outer-diameter: 33.25mm
//   inner-diameter: 27.88mm
arcade_button_inner_d = 28.1;
// Loudspeaker: 
//   Distance of holes: 43 mm
//   Square: 53mm
//   Inner circle: 47.32mm
loudspeaker_inner = 47.32;
loudspeaker_hd = 43;
// Screw
screw_shaft = 3.5;
screw_head = 6;

middle_x = size[0] / 2;
middle_y = size[1] / 2;

ls_y_delta = 20;
loudspeaker_trans = [middle_x, middle_y + ls_y_delta, 0];

half_ls = loudspeaker_hd /2;

union() {

	translate([loudspeaker_trans[0], loudspeaker_trans[1], 0]) {
		intersection() {
			linear_extrude(height=size[2]) {
				honeycomb_pattern(loudspeaker_inner, 1, 3);
			}
			cylinder(h=size[2], d=49, $fn=50);
		}
	}

	difference() {
		cube(size);

		translate([middle_x - arcade_button_inner_d - 10, arcade_button_inner_d, -0.1]) {
			cylinder(d=arcade_button_inner_d, h=size[2]+1, $fn=50);
		}

		translate([middle_x, arcade_button_inner_d, -0.1]) {
			cylinder(d=arcade_button_inner_d, h=size[2]+1, $fn=50);
		}

		translate([middle_x + arcade_button_inner_d + 10, arcade_button_inner_d, -0.1]) {
			cylinder(d=arcade_button_inner_d, h=size[2]+1, $fn=50);
		}

		translate(loudspeaker_trans) {
			cylinder(d=loudspeaker_inner, h=size[2]+1, $fn=50);
		}

		translate([5, 5, 0]) {
			screw();
		}

		translate([5, size[1] - 5, 0]) {
			screw();
		}

		translate([size[0] - 5, size[1] - 5, 0]) {
			screw();
		}

		translate([size[0] - 5, 5, 0]) {
			screw();
		}

		translate([middle_x - half_ls, middle_y - half_ls + ls_y_delta, 0]) {
			screw();
		}

		translate([middle_x + half_ls, middle_y - half_ls + ls_y_delta, 0]) {
			screw();
		}

		translate([middle_x - half_ls, middle_y + half_ls + ls_y_delta, 0]) {
			screw();
		}

		translate([middle_x + half_ls, middle_y + half_ls + ls_y_delta, 0]) {
			screw();
		}


	}
}

module honeycomb_pattern(size, line_size, line_space) {
	min_rad = (line_space / 2 * sqrt(3)) / 2 + line_size / 2;
	y_offset = sqrt(min_rad * min_rad * 4 - min_rad * min_rad);
	num_x = ceil(size / min_rad / 2) * 1.42;
	num_y = ceil(size / y_offset) * 1.42;
	difference() {
		square([size * 1.42, size * 1.42], center = true);
		for(y = [floor(-num_y / 2) : ceil(num_y / 2)]) {
			odd = (y % 2 == 0) ? 0 : min_rad;
			for(x = [floor(-num_x / 2) : ceil(num_x / 2)]) {
				translate([x * min_rad * 2 + odd, y * y_offset]) {
					rotate(30) {
						circle(d=line_space, $fn=6);
					}
				}
			}
		}
	}
}

module screw() {
	union() {
		translate([0, 0, -0.1]) {
			cylinder(d=screw_shaft, h=5.1, $fn=50);
		}
		translate([0, 0, 2.5]) {
			cylinder(d=screw_head, h=2.5, $fn=50);
		}
	}
}
