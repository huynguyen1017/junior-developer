module alu8(input [7:0] a, input [7:0] b, input [1:0] op, output [15:0] y, output overflow);
  real r_val;
  always @(*) r_val = $itor(a) / 3.14159;
  assign y = a + b;
  assign overflow = 1'b0;
endmodule
