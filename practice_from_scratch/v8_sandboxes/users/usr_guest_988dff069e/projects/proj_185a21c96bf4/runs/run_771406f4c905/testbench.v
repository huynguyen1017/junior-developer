`timescale 1ns/1ps
module sad_pe_comparator_tb;
    reg         clock = 0;
    reg         reset = 1;
    reg         start = 0;
    reg         valid_in = 0;
    reg  [7:0]  ref_pixel = 8'h00;
    reg  [7:0]  search_pixel = 8'h00;
    reg  [3:0]  cand_x = 4'h0;
    reg  [3:0]  cand_y = 4'h0;
    reg         row_done = 0;
    wire [15:0] accum_sad;
    wire [15:0] BestDist;
    wire [3:0]  motionX;
    wire [3:0]  motionY;
    wire        newBest;

    sad_pe_comparator dut (
        .clock(clock), .reset(reset), .start(start),
        .valid_in(valid_in), .ref_pixel(ref_pixel), .search_pixel(search_pixel),
        .cand_x(cand_x), .cand_y(cand_y), .row_done(row_done),
        .accum_sad(accum_sad), .BestDist(BestDist),
        .motionX(motionX), .motionY(motionY), .newBest(newBest)
    );

    always #1 clock = ~clock; // 500 MHz educational clock (2.0 ns period)

    integer i;
    initial begin
        $dumpfile("simulation.vcd");
        $dumpvars(0, sad_pe_comparator_tb);
        #4 reset = 0; start = 1;
        #2 start = 0;

        // Candidate 0 at (-8, -8) -> encoded as (4'h8, 4'h8) with +1 LSB mismatch across 256 pixels -> SAD = 16'h0100
        cand_x = 4'h8; cand_y = 4'h8;
        for (i = 0; i < 256; i = i + 1) begin
            @(negedge clock);
            valid_in = 1; ref_pixel = 8'h40; search_pixel = 8'h41;
        end
        @(negedge clock);
        valid_in = 0; row_done = 1;
        @(negedge clock);
        row_done = 0;
        $display("[CAND_0_CHECK] BestDist=0x%04h motionX=0x%01h motionY=0x%01h", BestDist, motionX, motionY);

        // Candidate 15 at (+7, -8) -> encoded as (4'h7, 4'h8) with exact match across 256 pixels -> SAD = 16'h0000
        cand_x = 4'h7; cand_y = 4'h8;
        for (i = 0; i < 256; i = i + 1) begin
            @(negedge clock);
            valid_in = 1; ref_pixel = 8'h5A; search_pixel = 8'h5A;
        end
        @(negedge clock);
        valid_in = 0; row_done = 1;
        @(negedge clock);
        row_done = 0;
        #4;
        $display("[CAND_15_CHECK] BestDist=0x%04h motionX=0x%01h motionY=0x%01h", BestDist, motionX, motionY);
        if (BestDist === 16'h0000 && motionX === 4'h7 && motionY === 4'h8) begin
            $display("JDEV_OPEN_EDA_VERIFIED: PASS (BestDist=0x0000, motionX=7, motionY=8)");
        end else begin
            $display("JDEV_OPEN_EDA_VERIFIED: FAIL");
            $fatal(1, "Simulation mismatch");
        end
        $finish;
    end
endmodule
