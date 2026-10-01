#!/bin/bash

# Captura o hostname atual do sistema
HOSTNAME_SISTEMA=$(hostname)
NOME_ARQUIVO="inventario_${HOSTNAME_SISTEMA}.txt"

# Executa o bloco de comandos e redireciona a saída para o arquivo dinâmico
{
  echo "=================================================="
  echo " INVENTÁRIO DO SISTEMA - COLETADO EM: $(date '+%Y-%m-%d %H:%M:%S')"
  echo " HOSTNAME: ${HOSTNAME_SISTEMA}"
  echo "=================================================="
  echo ""

  echo "=== HOSTNAME ==="
  hostnamectl
  echo ""

  echo "=== PROCESSADOR (CPU) ==="
  lscpu
  echo ""

  echo "=== MEMÓRIA RAM ==="
  free -h
  echo ""

  echo "=== REDE: INTERFACES ==="
  ip -br link
  echo ""

  echo "=== REDE: ENDEREÇOS IP ==="
  ip -br addr
  echo ""

  echo "=== REDE: ROTAS ==="
  ip route
  echo ""

  echo "=== SISTEMA OPERACIONAL ==="
  cat /etc/os-release
  echo ""

  echo "=== KERNEL ==="
  uname -a
  echo ""

  echo "=== PONTO DE MONTAGEM (/) ==="
  findmnt /
  echo ""

  echo "=== BTRFS: FILESYSTEM SHOW ==="
  btrfs filesystem show
  echo ""

  echo "=== BTRFS: FILESYSTEM USAGE ==="
  btrfs filesystem usage /
  echo ""

  echo "=== BTRFS: SUBVOLUMES ==="
  btrfs subvolume list /
  echo ""

  echo "=== PACOTES INSTALADOS (DPKG) ==="
  dpkg-query -W -f='${binary:Package}\t${Version}\n' | sort
} > "$NOME_ARQUIVO"

echo "Inventário gerado com sucesso no arquivo ${NOME_ARQUIVO}!"
