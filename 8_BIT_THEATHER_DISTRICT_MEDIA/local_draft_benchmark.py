#!/usr/bin/env python3
import os
import sys
import time
import json

# Terminal styling utilities matching 8-Bit Theater District aesthetic
class TerminalColors:
    HEADER = '\033[95m'
    CYAN = '\033[36m'
    PINK = '\033[38;5;205m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    banner = f"""
{TerminalColors.CYAN}{TerminalColors.BOLD}====================================================================
  8-BIT THEATER DISTRICT - HETEROGENEOUS DRAFT INFERENCE BENCHMARK
===================================================================={TerminalColors.ENDC}
Optimized for AMD Ryzen 7 6800U (Radeon 680M) | Local-First SRE Pipeline
    """
    print(banner)

try:
    import torch
    import torch.nn as nn
except ImportError:
    print_banner()
    print(f"{TerminalColors.FAIL}[ERROR]{TerminalColors.ENDC} PyTorch is not installed on this Python environment.")
    print(f"Please run: {TerminalColors.BOLD}pip install torch{TerminalColors.ENDC} to execute the benchmark.")
    sys.exit(1)

class MockDraftModel(nn.Module):
    """Simulates a lightweight draft model structure (e.g., small transformer layer)"""
    def __init__(self, d_model=1024, num_layers=4):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.TransformerEncoderLayer(d_model=d_model, nhead=8, dim_feedforward=2048, batch_first=True)
            for _ in range(num_layers)
        ])
        self.lm_head = nn.Linear(d_model, 32000, bias=False) # standard vocab size

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return self.lm_head(x)

def run_benchmark(device, model, x, num_runs=100):
    # Warmup
    for _ in range(10):
        _ = model(x)
    if device.type == 'cuda':
        torch.cuda.synchronize()
    
    latencies = []
    for _ in range(num_runs):
        start = time.perf_counter()
        _ = model(x)
        if device.type == 'cuda':
            torch.cuda.synchronize()
        end = time.perf_counter()
        latencies.append((end - start) * 1000) # convert to ms
        
    return latencies

def main():
    print_banner()
    
    # Configuration
    d_model = 1024
    num_layers = 4
    batch_size = 1
    seq_len = 8 # Simulating K=8 draft tokens
    num_runs = 100
    
    print(f"{TerminalColors.BOLD}Benchmark Parameters:{TerminalColors.ENDC}")
    print(f"  - Draft Sequence Length (K): {seq_len} tokens")
    print(f"  - Model Dimensions (d_model): {d_model}")
    print(f"  - Transformer Layers: {num_layers}")
    print(f"  - Warmup Runs: 10 | Benchmark Runs: {num_runs}\n")

    # Instantiate Model
    print(f"{TerminalColors.CYAN}[INIT]{TerminalColors.ENDC} Initializing lightweight draft architecture...")
    cpu_model = MockDraftModel(d_model=d_model, num_layers=num_layers)
    cpu_model.eval()
    
    # CPU Input
    cpu_input = torch.randn(batch_size, seq_len, d_model)
    
    # 1. CPU Benchmarking (Thread counts scaling)
    print(f"\n{TerminalColors.BOLD}1. CPU Benchmarking (AMD Ryzen 7 6800U){TerminalColors.ENDC}")
    cpu_threads = [1, 4, 8, 16]
    cpu_results = {}
    
    for threads in cpu_threads:
        torch.set_num_threads(threads)
        print(f"  Running on CPU with {threads} threads...", end="", flush=True)
        with torch.no_grad():
            latencies = run_benchmark(torch.device('cpu'), cpu_model, cpu_input, num_runs=num_runs)
        
        avg_lat = sum(latencies) / len(latencies)
        p99_lat = sorted(latencies)[int(num_runs * 0.99) - 1]
        cpu_results[f"threads_{threads}"] = {
            "avg_ms": avg_lat,
            "p99_ms": p99_lat
        }
        print(f" {TerminalColors.GREEN}Avg: {avg_lat:.2f}ms | P99: {p99_lat:.2f}ms{TerminalColors.ENDC}")
        
    # 2. GPU Benchmarking (Radeon 680M via CUDA/ROCm)
    gpu_available = torch.cuda.is_available()
    gpu_results = {}
    
    print(f"\n{TerminalColors.BOLD}2. GPU Benchmarking (AMD Radeon 680M){TerminalColors.ENDC}")
    if gpu_available:
        device = torch.device('cuda')
        print(f"  {TerminalColors.GREEN}[FOUND]{TerminalColors.ENDC} ROCm/CUDA device active: {torch.cuda.get_device_name(0)}")
        print(f"  Moving model and input to GPU...", end="", flush=True)
        gpu_model = cpu_model.to(device)
        gpu_input = cpu_input.to(device)
        print(" Done.")
        
        print("  Running on GPU...", end="", flush=True)
        with torch.no_grad():
            latencies = run_benchmark(device, gpu_model, gpu_input, num_runs=num_runs)
        avg_lat = sum(latencies) / len(latencies)
        p99_lat = sorted(latencies)[int(num_runs * 0.99) - 1]
        gpu_results = {
            "available": True,
            "avg_ms": avg_lat,
            "p99_ms": p99_lat
        }
        print(f" {TerminalColors.GREEN}Avg: {avg_lat:.2f}ms | P99: {p99_lat:.2f}ms{TerminalColors.ENDC}")
    else:
        print(f"  {TerminalColors.WARNING}[WARN]{TerminalColors.ENDC} ROCm/CUDA GPU is not available in this PyTorch build.")
        print("  (If running on Beelink SER5 MAX, ensure PyTorch is compiled with ROCm support.)")
        gpu_results = {
            "available": False,
            "avg_ms": None,
            "p99_ms": None
        }

    # Summary Report
    print(f"\n{TerminalColors.CYAN}{TerminalColors.BOLD}===================================================================={TerminalColors.ENDC}")
    print(f"{TerminalColors.PINK}{TerminalColors.BOLD}                      BENCHMARK CONCLUSION                          {TerminalColors.ENDC}")
    print(f"{TerminalColors.CYAN}{TerminalColors.BOLD}===================================================================={TerminalColors.ENDC}")
    
    # Find best CPU thread count
    best_threads = min(cpu_results.items(), key=lambda x: x[1]["avg_ms"])
    print(f"Best CPU Configuration: {TerminalColors.BOLD}{best_threads[0].replace('_', ' ')}{TerminalColors.ENDC} ({best_threads[1]['avg_ms']:.2f}ms avg)")
    
    if gpu_results["available"]:
        ratio = best_threads[1]["avg_ms"] / gpu_results["avg_ms"]
        if ratio > 1:
            print(f"GPU vs Best CPU Speedup: {TerminalColors.GREEN}{ratio:.2fx} Faster on GPU{TerminalColors.ENDC}")
        else:
            print(f"GPU vs Best CPU Speedup: {TerminalColors.WARNING}{1/ratio:.2fx} Faster on CPU (Common for small batches/sequences due to GPU scheduling overhead){TerminalColors.ENDC}")
    else:
        print("GPU benchmark skipped due to missing ROCm/CUDA context.")
        
    print(f"{TerminalColors.CYAN}===================================================================={TerminalColors.ENDC}")

    # Export to JSON
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_results": cpu_results,
        "gpu_results": gpu_results
    }
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n{TerminalColors.GREEN}[SUCCESS]{TerminalColors.ENDC} Results exported to {TerminalColors.BOLD}benchmark_results.json{TerminalColors.ENDC}")

if __name__ == "__main__":
    main()
