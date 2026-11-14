`timescale 1ns/1ps
module tb_no_assert;
  reg [7:0] a = 8'h10, b = 8'h20;
  reg [1:0] op = 2'b00;
  wire [15:0] y;
  wire ovf;
  alu8 dut(.a(a), .b(b), .op(op), .y(y), .overflow(ovf));
  initial begin
    $dumpfile("simulation.vcd");
    $dumpvars(0, tb_no_assert);
    #10 a = 8'h30; b = 8'h40;
    #10 op = 2'b01;
    #10 a = 8'h90; b = 8'h10;
    #10 $display("Simulation finished without self-check assertions.");
    $finish;
  end
endmodule