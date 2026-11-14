`timescale 1ns/1ps
// JUNIOR DEVELOPER — Lesson 1: 16-Bit Non-Saturating SAD Accumulator & BestDist Comparator
module sad_pe_comparator (
    input  wire        clock,
    input  wire        reset,
    input  wire        start,
    input  wire        valid_in,
    input  wire [7:0]  ref_pixel,
    input  wire [7:0]  search_pixel,
    input  wire [3:0]  cand_x,
    input  wire [3:0]  cand_y,
    input  wire        row_done,
    output reg  [15:0] accum_sad,
    output reg  [15:0] BestDist,
    output reg  [3:0]  motionX,
    output reg  [3:0]  motionY,
    output reg         newBest
);
    wire [7:0] abs_diff = (ref_pixel >= search_pixel) ? (ref_pixel - search_pixel) : (search_pixel - ref_pixel);

    always @(posedge clock) begin
        if (reset || start) begin
            accum_sad <= 16'h0000;
            BestDist  <= 16'hFFFF;
            motionX   <= 4'h0;
            motionY   <= 4'h0;
            newBest   <= 1'b0;
        end else begin
            newBest <= 1'b0;
            if (valid_in) begin
                accum_sad <= accum_sad + {8'h00, abs_diff};
            end
            if (row_done) begin
                if (accum_sad < BestDist) begin
                    BestDist <= accum_sad;
                    motionX  <= cand_x;
                    motionY  <= cand_y;
                    newBest  <= 1'b1;
                end
                accum_sad <= 16'h0000;
            end
        end
    end
endmodule

// E2E_USER_EDIT_MARKER_2026
