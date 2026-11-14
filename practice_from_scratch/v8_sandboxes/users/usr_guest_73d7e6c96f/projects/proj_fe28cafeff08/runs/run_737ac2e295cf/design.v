module alu8(input [7:0] a, input [7:0] b, input [1:0] op, output [15:0] y, output overflow);
  assign y = a + b;
  assign overflow = 1'b0;
  `ifndef __ICARUS__
  yosys_only_syntax_error bad_cell;
  `endif
endmodule