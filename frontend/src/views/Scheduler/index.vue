<template>
  <div class="scheduler-page" ref="containerRef">
    <div class="scheduler-app">
      <div class="toolbar">
        <div class="brand">CS Roster<small>客服中台排班</small></div>
        <div class="sep"></div>
        <div class="month-nav">
          <button class="btn" id="prevMonth" title="上一月">‹</button>
          <div class="month-label" id="monthLabel">—</div>
          <button class="btn" id="nextMonth" title="下一月">›</button>
          <button class="btn" id="todayBtn" title="回到本月">今</button>
          <button class="btn" id="viewModeBtn" title="切换单月 / 3 个月">3 月</button>
        </div>
        <div class="sep"></div>
        <button class="btn primary" id="autoGen">自动初排</button>
        <button class="btn" id="clearMonth" title="清空本月排班（保留 AL/離港）">清空排班</button>
        <div class="sep"></div>
        <button class="btn" id="undoBtn" title="撤销上一步 (Ctrl+Z)">↩ 撤销</button>
        <div class="sep"></div>
        <button class="btn" id="importBtn">导入</button>
        <button class="btn" id="exportBtn">导出</button>
        <button class="btn" id="staffBtn" title="编辑人员配置">人员</button>
        <button class="btn" id="shiftBtn" title="编辑班次时间">班次</button>
        <div class="sep"></div>
        <button class="btn" id="zoomOut" title="缩小">−</button>
        <span class="zoom-label" id="zoomLabel">100%</span>
        <button class="btn" id="zoomIn" title="放大">+</button>
        <button class="btn" id="zoomReset" title="重置缩放">1:1</button>
        <div class="grow"></div>
        <button class="btn danger" id="resetAll" title="清空所有数据（含所有月份）">重置</button>
      </div>

      <div class="main">
        <div class="panel">
          <div class="grid-wrap">
            <div class="grid" id="grid"></div>
          </div>
          <div class="kpi-row" id="kpiRow"></div>
        </div>

        <div class="side">
          <div class="panel">
            <h3>班次图例 <button class="link-btn" id="editShiftFromLegend" style="float:right;padding:0 4px;font-size:11px;text-transform:none;">编辑时间…</button></h3>
            <div class="legend" id="legend"></div>
            <div class="legend-note">
              单击单元格 = 下拉选班次；拖选或 Shift+点击 = 多选后底部批量填；键盘 <span class="kbd" style="display:inline-block;padding:0 4px;background:var(--surface-2);border:1px solid var(--border);border-radius:3px;font-family:monospace;font-size:10.5px;">1-9</span> 也能填。
            </div>
          </div>

          <div class="panel">
            <h3>合规审计（本月）</h3>
            <div id="auditPanel"></div>
          </div>

          <div class="panel">
            <h3>每日覆盖 · 早/中/晚</h3>
            <div id="dailyCoverage" style="max-height: 260px; overflow: auto;"></div>
          </div>

          <div class="panel">
            <h3>团队一览</h3>
            <div id="teamOverview" style="max-height: 260px; overflow: auto;"></div>
          </div>
        </div>
      </div>

      <footer class="foot">
        <span>单击 = 下拉选</span>
        <span>拖选 / <span class="kbd">Shift</span>+点击 = 多选</span>
        <span><span class="kbd">1-9</span> 早/正/中/晚/周早/周晚/SB 填班</span>
        <span><span class="kbd">A</span> AL <span class="kbd">O</span> 離港 <span class="kbd">R</span> 补休</span>
        <span><span class="kbd">Del</span> 清空 <span class="kbd">Ctrl+Z</span> 撤销 <span class="kbd">Esc</span> 取消</span>
        <span style="margin-left:auto;">数据自动同步到服务器 · 团队共享</span>
      </footer>
    </div>

    <div class="picker" id="picker"></div>
    <div class="batchbar" id="batchbar"></div>
    <div class="modal-bg" id="modalBg">
      <div class="modal" id="modal">
        <header><h2 id="modalTitle">—</h2><div class="grow"></div><button class="link-btn" id="modalClose">关闭</button></header>
        <div class="m-body" id="modalBody"></div>
        <footer id="modalFoot"></footer>
      </div>
    </div>
    <div class="toast" id="toast">saved</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { initScheduler, destroyScheduler } from './scheduler-core'

const containerRef = ref<HTMLElement>()

onMounted(() => {
  if (containerRef.value) {
    initScheduler()
  }
})

onBeforeUnmount(() => {
  destroyScheduler()
})
</script>

<style src="./scheduler.css"></style>
