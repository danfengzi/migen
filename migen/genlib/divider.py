from migen.fhdl.structure import *

class Divider:
	def __init__(self, w):
		self.w = w
		
		self.start_i = Signal()
		self.dividend_i = Signal(w)
		self.divisor_i = Signal(w)
		self.ready_o = Signal()
		self.quotient_o = Signal(w)
		self.remainder_o = Signal(w)
	
	def get_fragment(self):
		w = self.w
		
		qr = Signal(2*w)
		counter = Signal(max=w+1)
		divisor_r = Signal(w)
		diff = Signal(w+1)
		
		comb = [
			self.quotient_o.eq(qr[:w]),
			self.remainder_o.eq(qr[w:]),
			self.ready_o.eq(counter == 0),
			diff.eq(self.remainder_o - divisor_r)
		]
		sync = [
			If(self.start_i,
				counter.eq(w),
				qr.eq(self.dividend_i),
				divisor_r.eq(self.divisor_i)
			).Elif(~self.ready_o,
					If(diff[w],
						qr.eq(Cat(0, qr[:2*w-1]))
					).Else(
						qr.eq(Cat(1, qr[:w-1], diff[:w]))
					),
					counter.eq(counter - 1)
			)
		]
		return Fragment(comb, sync)
