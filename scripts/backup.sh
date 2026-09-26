#!/usr/bin/env bash
# ──────────────────────────────────────────────
#  南无那面 · 仁格智能体  数据备份脚本
#  定期将记忆数据与知识图谱数据备份至指定位置。
#
#  用法:
#    ./scripts/backup.sh                          # 备份到默认位置 (./backups/)
#    ./scripts/backup.sh /path/to/backup_dir      # 备份到指定目录
#    BACKUP_RETAIN_DAYS=30 ./scripts/backup.sh    # 保留最近30天的备份
#
#  推荐通过 crontab 定时执行:
#    0 2 * * * /app/scripts/backup.sh /backups
# ──────────────────────────────────────────────

set -euo pipefail

# ── 配置 ──
BACKUP_DIR="${1:-./backups}"
RETAIN_DAYS="${BACKUP_RETAIN_DAYS:-7}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="namian_backup_${TIMESTAMP}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# 数据源路径
DATA_DIR="${DATA_DIR:-./data}"
MEMORY_FILE="${MEMORY_STORAGE_PATH:-${DATA_DIR}/memories.json}"
KG_FILE="${KG_STORAGE_PATH:-${DATA_DIR}/knowledge_graph.json}"

# ── 颜色 ──
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

# ── 函数 ──
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ── 主流程 ──
log_info "南无那面 数据备份开始..."
log_info "备份目录: ${BACKUP_DIR}"

# 创建备份目录
mkdir -p "${BACKUP_PATH}"

# 1. 备份记忆数据
if [ -f "${MEMORY_FILE}" ]; then
    cp "${MEMORY_FILE}" "${BACKUP_PATH}/memories.json"
    MEM_SIZE=$(wc -c < "${MEMORY_FILE}")
    log_info "记忆数据已备份 (${MEM_SIZE} bytes)"
else
    log_warn "记忆数据文件不存在: ${MEMORY_FILE}，跳过"
fi

# 2. 备份知识图谱数据
if [ -f "${KG_FILE}" ]; then
    cp "${KG_FILE}" "${BACKUP_PATH}/knowledge_graph.json"
    KG_SIZE=$(wc -c < "${KG_FILE}")
    log_info "知识图谱数据已备份 (${KG_SIZE} bytes)"
else
    log_warn "知识图谱数据文件不存在: ${KG_FILE}，跳过"
fi

# 3. 备份道德语法模式库
PATTERNS_FILE="${DATA_DIR}/moral_syntax/patterns_regex.json"
if [ -f "${PATTERNS_FILE}" ]; then
    cp "${PATTERNS_FILE}" "${BACKUP_PATH}/patterns_regex.json"
    log_info "道德语法模式库已备份"
fi

# 4. 压缩备份
cd "${BACKUP_DIR}"
tar -czf "${BACKUP_NAME}.tar.gz" "${BACKUP_NAME}"
rm -rf "${BACKUP_PATH}"
log_info "备份已压缩: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"

# 5. 清理过期备份
if [ -d "${BACKUP_DIR}" ]; then
    DELETED_COUNT=$(find "${BACKUP_DIR}" -name "namian_backup_*.tar.gz" -type f -mtime +${RETAIN_DAYS} -delete -print | wc -l)
    if [ "${DELETED_COUNT}" -gt 0 ]; then
        log_info "已清理 ${DELETED_COUNT} 个过期备份（保留${RETAIN_DAYS}天）"
    fi
fi

log_info "备份完成。"




