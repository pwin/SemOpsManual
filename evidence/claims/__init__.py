"""Every claim, in manual order: the README, chapters 1 to 15, then Appendix A."""
from . import ch00, ch01, ch02, ch03, ch04, ch05, ch06, ch07, ch08, ch09, ch10, ch11, ch12, ch13, ch14, ch15, chA

MODULES = (ch00, ch01, ch02, ch03, ch04, ch05, ch06, ch07, ch08, ch09, ch10, ch11, ch12, ch13, ch14, ch15, chA)
ALL = [c for m in MODULES for c in m.CLAIMS]
