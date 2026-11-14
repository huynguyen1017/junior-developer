`timescale 1ns/1ps
module motion_estimator_edu_tb;
    reg         clock = 0;
    reg         start = 0;
    wire [12:0] count;
    wire [15:0] newDist;
    wire [15:0] PEready;
    wire [3:0]  VectorX;
    wire [3:0]  VectorY;
    wire        newBest;
    wire [15:0] BestDist;
    wire [3:0]  motionX;
    wire [3:0]  motionY;
    wire        completed;

    motion_estimator_edu_top dut (
        .clock(clock), .start(start), .count(count),
        .newDist(newDist), .PEready(PEready),
        .VectorX(VectorX), .VectorY(VectorY),
        .newBest(newBest), .BestDist(BestDist),
        .motionX(motionX), .motionY(motionY), .completed(completed)
    );

    always #1 clock = ~clock;

    initial begin
        $dumpfile("simulation.vcd");
        $dumpvars(0, motion_estimator_edu_tb);
        start = 0;
        #6 start = 1;
        wait (count == 13'h0100);
        #1;
        $display("[ROW1_PE0] count=0x%04h BestDist=0x%04h motionX=0x%01h motionY=0x%01h", count, BestDist, motionX, motionY);
        wait (completed == 1'b1);
        #2;
        $display("[ROW1_PE15_FINAL] count=0x%04h BestDist=0x%04h motionX=0x%01h motionY=0x%01h completed=%b", count, BestDist, motionX, motionY, completed);
        if (BestDist === 16'h0000 && motionX === 4'h7 && motionY === 4'h8 && completed === 1'b1) begin
            $display("JDEV_OPEN_EDA_VERIFIED: PASS (Motion Estimator 16-Bit BestDist=0x0000, motionX=7, motionY=8)");
        end else begin
            $display("JDEV_OPEN_EDA_VERIFIED: FAIL");
            $fatal(1, "Motion Estimator verification failed");
        end
        $finish;
    end
endmodule
