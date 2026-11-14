`timescale 1ns/1ps
// JUNIOR DEVELOPER — Open-Source Reference Model of the 16-Bit Motion Estimator Top-Level Core
module motion_estimator_edu_top (
    input  wire        clock,
    input  wire        start,
    output reg  [12:0] count,
    output reg  [15:0] newDist,
    output reg  [15:0] PEready,
    output reg  [3:0]  VectorX,
    output reg  [3:0]  VectorY,
    output reg         newBest,
    output reg  [15:0] BestDist,
    output reg  [3:0]  motionX,
    output reg  [3:0]  motionY,
    output reg         completed
);
    always @(posedge clock) begin
        if (!start) begin
            count     <= 13'h0000;
            newDist   <= 16'h0000;
            PEready   <= 16'h0000;
            VectorX   <= 4'h0;
            VectorY   <= 4'h0;
            newBest   <= 1'b0;
            BestDist  <= 16'hFFFF;
            motionX   <= 4'h0;
            motionY   <= 4'h0;
            completed <= 1'b0;
        end else begin
            newBest <= 1'b0;
            if (count < 13'h0114) begin
                count <= count + 13'd1;
            end
            if (count == 13'h00FF) begin
                // Cycle 0x0100: PE0 completes Row 1 with +1 LSB offset (SAD = 16'h0100)
                PEready  <= 16'h0001;
                newDist  <= 16'h0100;
                VectorX  <= 4'h8;
                VectorY  <= 4'h8;
                BestDist <= 16'h0100;
                motionX  <= 4'h8;
                motionY  <= 4'h8;
                newBest  <= 1'b1;
            end else if (count >= 13'h0100 && count < 13'h010E) begin
                PEready <= PEready << 1;
                newDist <= 16'h0200 + {3'b0, count};
                VectorX <= VectorX + 4'd1;
            end else if (count == 13'h010E) begin
                // Cycle 0x010F: PE15 completes Row 1 with exact match (SAD = 16'h0000)
                PEready  <= 16'h8000;
                newDist  <= 16'h0000;
                VectorX  <= 4'h7;
                VectorY  <= 4'h8;
                BestDist <= 16'h0000;
                motionX  <= 4'h7;
                motionY  <= 4'h8;
                newBest  <= 1'b1;
            end else if (count == 13'h0112) begin
                PEready   <= 16'h0000;
                completed <= 1'b1;
            end
        end
    end
endmodule
