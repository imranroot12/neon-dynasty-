"""Small environment compatibility layer for the Stake Math SDK.

This is NOT a replacement for the official `zstandard` Python package in a
production deployment. It exists only so the SDK can use the system `zstd`
CLI in restricted build environments where PyPI is unavailable.
"""
import subprocess
class _Writer:
    def __init__(self, f): self.f=f; self.buf=bytearray()
    def __enter__(self): return self
    def write(self,b): self.buf.extend(b); return len(b)
    def __exit__(self,*_):
        self.f.write(subprocess.run(['zstd','-q','-c','-T0'], input=bytes(self.buf), stdout=subprocess.PIPE, check=True).stdout)
class ZstdCompressor:
    def compress(self, data):
        return subprocess.run(['zstd','-q','-c','-T0'], input=data, stdout=subprocess.PIPE, check=True).stdout
    def stream_writer(self,f,closefd=False): return _Writer(f)
class _Reader:
    def __init__(self,f): self.f=f
    def __enter__(self): self.data=subprocess.run(['zstd','-q','-d','-c'], input=self.f.read(), stdout=subprocess.PIPE, check=True).stdout; self.pos=0; return self
    def read(self,n=-1):
        if n < 0: n=len(self.data)-self.pos
        out=self.data[self.pos:self.pos+n]; self.pos += len(out); return out
    def __exit__(self,*_): pass
class ZstdDecompressor:
    def decompress(self, data):
        return subprocess.run(['zstd','-q','-d','-c'], input=data, stdout=subprocess.PIPE, check=True).stdout
    def stream_reader(self,f): return _Reader(f)
