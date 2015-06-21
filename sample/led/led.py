import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from veriloggen import *

def mkLed():
    m = Module('blinkled')
    width = m.Parameter('WIDTH', 8)
    clk = m.Input('CLK')
    rst = m.Input('RST')
    led = m.OutputReg('LED', width)
    count = m.Reg('count', 32)

    m.Always(Posedge(clk),
             [ If(rst,
                  [ count.set(0) ],
                  [ count.set(count + 1) ])])
    
    m.Always(Posedge(clk),
             [ If(rst,
                  [ led.set(0) ],
                  [ If(count == 1024 - 1,
                       [ led.set(led + 1) ])])])
    
    return m

#-------------------------------------------------------------------------------
led = mkLed()
verilog = led.toVerilog()
print(verilog)

#-------------------------------------------------------------------------------
expected_verilog = """
module blinkled #
  ( 
   parameter WIDTH = 8
  )
  ( 
   input CLK, 
   input RST,
   output reg [WIDTH-1:0] LED
  );
  reg [32-1:0] count;

  always @(posedge CLK) begin
    if(RST) begin
      count <= 0;
    end else begin
      count <= count + 1;
    end
  end
  always @(posedge CLK) begin
    if(RST) begin
      LED <= 0;
    end else begin
      if(count == 1023) begin
        LED <= LED + 1;
      end 
    end
  end
endmodule
"""

#from pyverilog.vparser.parser import VerilogParser
#from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
#parser = VerilogParser()
#expected_verilog_ast = parser.parse(expected_verilog)
#codegen = ASTCodeGenerator()
#expected_verilog_code = codegen.visit(expected_verilog_ast)

#print('// Sample Verilog code -> AST -> Verilog code')
#print(expected_verilog_code)

#import difflib
#diff = difflib.unified_diff(verilog.splitlines(), expected_verilog_code.splitlines())
#print('\n'.join(list(diff)))
