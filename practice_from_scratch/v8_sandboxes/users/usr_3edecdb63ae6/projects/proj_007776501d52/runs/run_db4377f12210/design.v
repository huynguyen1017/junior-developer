module alu8(input [7:0] a, input [7:0] b, input [1:0] op, output [15:0] y, output overflow);
  assign y = (op == 2'b00) ? (a + b) : ((op == 2'b01) ? (a - b) : (a * b));
  assign overflow = (y > 16'h00FF);
endmodule
