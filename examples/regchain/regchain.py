from __future__ import absolute_import
from __future__ import print_function
import os
import sys

# the next line can be removed after installation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from veriloggen import *

def mkRegChain(length=120, width=8):
    m = Module("reg_chain")

    clk = m.Input('CLK')
    rst = m.Input('RST')
    sw = m.Input('sw', 8)
    dout = m.Output('dout', width)

    seq = Seq(m, 'seq', clk, rst)

    update_cond_value = m.TmpReg(3, initval=0)
    seq.add( update_cond_value(sw[2:0]) )

    area_size = m.TmpReg(2, initval=0)
    seq.add( area_size(sw[4:3]) )
    
    count = m.TmpReg(2, initval=0)
    seq.add( count.inc() )
    
    update_cond = m.TmpReg(initval=0)
    seq.add( update_cond(count < update_cond_value) )

    orig = m.TmpReg(width, initval=0)
    prev = orig

    regs = []
    
    for i in range(length):
        area_id = i // (length // 4)
        r = m.TmpReg(width, initval=0)
        regs.append(r)
        seq.add( r(prev + 1), cond=AndList(update_cond, area_id <= area_size) )
        prev = r

    seq.add( orig(regs[1*length//4-1] + 3), cond=AndList(update_cond, area_size==0) )
    seq.add( orig(regs[2*length//4-1] + 2), cond=AndList(update_cond, area_size==1) )
    seq.add( orig(regs[3*length//4-1] + 1), cond=AndList(update_cond, area_size==2) )
    seq.add( orig(regs[4*length//4-1] + 0), cond=AndList(update_cond, area_size==3) )

    seq.make_always()
    
    m.Assign( dout(orig) )

    return m

def mkTest(length=120, width=8):
    m = Module('test')
    
    main = mkRegChain(length, width)
    params = m.copy_params(main)
    ports = m.copy_sim_ports(main)
    
    clk = ports['CLK']
    rst = ports['RST']
    sw = ports['sw']
    dout = ports['dout']

    fsm = FSM(m, 'fsm', clk, rst)
    count = m.TmpReg(32, initval=0)
    
    fsm.add( sw((3 << 3) | 4) )
    fsm.add( count.inc() )
    fsm.add( count(0), cond=count==2000 )
    fsm.goto_next(count==2000)

    fsm.add( sw((2 << 3) | 4) )
    fsm.add( count.inc() )
    fsm.add( count(0), cond=count==2000 )
    fsm.goto_next(count==2000)

    fsm.add( sw((1 << 3) | 4) )
    fsm.add( count.inc() )
    fsm.add( count(0), cond=count==2000 )
    fsm.goto_next(count==2000)

    fsm.add( sw((0 << 3) | 4) )
    fsm.add( count.inc() )
    fsm.add( count(0), cond=count==2000 )
    fsm.goto_next(count==2000)

    fsm.add( sw((2 << 3) | 3) )
    fsm.add( count.inc() )
    fsm.add( count(0), cond=count==2000 )
    fsm.goto_next(count==2000)

    fsm.add( sw((2 << 3) | 2) )
    fsm.add( count.inc() )
    fsm.add( count(0), cond=count==2000 )
    fsm.goto_next(count==2000)

    fsm.add( sw((2 << 3) | 1) )
    fsm.add( count.inc() )
    fsm.add( count(0), cond=count==2000 )
    fsm.goto_next(count==2000)

    fsm.add( sw((2 << 3) | 0) )
    fsm.add( count.inc() )
    fsm.add( count(0), cond=count==2000 )
    fsm.goto_next(count==2000)

    fsm.make_always()
    
    uut = m.Instance(main, 'uut',
                     params=m.connect_params(main),
                     ports=m.connect_ports(main))

    simulation.setup_waveform(m, uut, m.get_vars())
    simulation.setup_clock(m, clk, hperiod=5)
    init = simulation.setup_reset(m, rst, m.make_reset(), period=100)

    nclk = simulation.next_clock
    
    init.add(
        sw(0),
        Delay(1000 * 200),
        Systask('finish'),
    )

    return m
    
if __name__ == '__main__':
    main = mkRegChain(length=120)
    verilog = main.to_verilog('tmp.v')
    print(verilog)

    #test = mkTest()
    #verilog = test.to_verilog('tmp.v')
    #print(verilog)

    # run simulator (Icarus Verilog)
    #sim = simulation.Simulator(test)
    #rslt = sim.run() # display=False
    ##rslt = sim.run(display=True)
    #print(rslt)

    # launch waveform viewer (GTKwave)
    #sim.view_waveform() # background=False
    #sim.view_waveform(background=True)
