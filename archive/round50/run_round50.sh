#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
python round50_krawczyk_certifier.py \
  --nodes-csv data/round43_full_hierarchy_nodes_weights.csv \
  --alternation-csv data/round43_full_hierarchy_alternation.csv \
  --output-dir results
python round50_jacobian_audit.py \
  --nodes-csv data/round43_full_hierarchy_nodes_weights.csv \
  --alternation-csv data/round43_full_hierarchy_alternation.csv \
  --output results/round50_jacobian_audit.csv
python round50_global_minimax_audit.py \
  --nodes-csv data/round43_full_hierarchy_nodes_weights.csv \
  --alternation-csv data/round43_full_hierarchy_alternation.csv \
  --output-dir results
python create_round50_manifest.py
