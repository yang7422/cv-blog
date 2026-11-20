---
layout: page
title: Robotics from the Ground Up
description: "Weekly undergraduate lab seminars, Dec. 2019 – Jul. 2021: servo packets built by hand, a legged robot, and a robot that follows a person"
img: assets/img/projects/ground-up-robotics/thumb.webp
importance: 1
---

<!-- Seminar data: _data/ground_up_seminars.yml. Styles: the "Project page: Robotics from the Ground Up" block in _sass/_custom.scss. -->

{%- assign seminars = site.data.ground_up_seminars -%}

Before graduate school, I spent 19 months as an undergraduate researcher at IHLAB (Tech University of Korea) and gave a lab seminar almost every week. Each one covered what I had planned, built and measured, what broke, and what I would fix by the next week.
The work ran from a single servo on a bare microcontroller to a robot that follows a person. This page condenses that archive into the parts that still describe how I work.

<div class="gur-stats">
  <div class="gur-stat"><span class="gur-stat-value">{{ seminars.size }}</span><span class="gur-stat-label">lab seminars, almost one a week</span></div>
  <div class="gur-stat"><span class="gur-stat-value">19</span><span class="gur-stat-label">months, <span class="nobr">Dec. 2019 – Jul. 2021</span></span></div>
  <div class="gur-stat"><span class="gur-stat-value">600+</span><span class="gur-stat-label">slides of plans, measurements and fixes</span></div>
  <div class="gur-stat"><span class="gur-stat-value">40</span><span class="gur-stat-label">test videos of robots, boards and scope traces</span></div>
</div>

## How I work

<div class="gur-traits">
  <div class="gur-trait">
    <strong>Start at the wire</strong>
    <p>I wrote the <span class="nobr">low-level</span> code myself: DYNAMIXEL packets byte by byte on an ATmega128, and an nRF24L01+ radio driver at register level. I checked the traffic on an oscilloscope or a logic analyzer.</p>
  </div>
  <div class="gur-trait">
    <strong>Measure against ground truth</strong>
    <p>Foot positions were traced on paper, ranges were taped out on a floor grid, and radio timing was logged over 519 exchanges. A number only counted once it had been checked.</p>
  </div>
  <div class="gur-trait">
    <strong>Fix causes, not symptoms</strong>
    <p>When a filter would only have hidden a problem, I kept digging. Range spikes turned out to be reflections, timing jitter a slow <span class="nobr">status-register</span> read, and a silent radio a CE pin that was never raised.</p>
  </div>
  <div class="gur-trait">
    <strong>Write it all down, dead ends included</strong>
    <p>Every talk opens with the plan and ends with open questions. "Not solved yet" appears often, and so does a <span class="nobr">wide-angle</span> receiver I could not make work, measured and explained rather than quietly dropped.</p>
  </div>
</div>

## Seminar timeline

<!-- Timeline: one square per seminar, one column per week (week 0 starts Mon 16 Dec 2019).
     Wide screens get the annotated SVG; narrow ones a full-width bar strip plus the list below it. -->
{%- assign t0 = '2019-12-16' | date: '%s' | plus: 0 -%}
{%- capture gur_cells -%}
{%- for w in (0..82) -%}
<rect class="gur-empty" x="{{ w | times: 10 | plus: 10 }}" y="56" width="8" height="8" rx="2"/>
{%- endfor -%}
{%- assign prev = -1 -%}
{%- assign stack = 0 -%}
{%- for s in seminars -%}
{%- assign ts = s.date | date: '%s' | plus: 0 -%}
{%- assign wk = ts | minus: t0 | divided_by: 604800 -%}
{%- if wk == prev -%}{%- assign stack = stack | plus: 1 -%}{%- else -%}{%- assign stack = 0 -%}{%- endif -%}
{%- assign prev = wk -%}
{%- assign x = wk | times: 10 | plus: 10 -%}
{%- assign y = stack | times: 10 -%}
{%- assign y = 56 | minus: y -%}
<rect class="gur-cell" x="{{ x }}" y="{{ y }}" width="8" height="8" rx="2" data-date="{{ s.date | date: '%b %-d, %Y' }}" data-topic="{{ s.topic | escape }}"/>
{%- endfor -%}
{%- endcapture -%}
{%- assign phase_names = 'Servo packets to a legged robot|Ultrasonic following unit and own boards|Graduation project: a person-following robot' | split: '|' -%}
<div class="gur-timeline" id="gur-timeline">
<svg class="gur-tl-wide" viewBox="0 0 850 128" role="img" tabindex="0" aria-labelledby="gur-tl-title gur-tl-desc">
<title id="gur-tl-title">Seminar timeline</title>
<desc id="gur-tl-desc">{{ seminars.size }} seminars from December 2019 to July 2021: one square per seminar, one column per week. Arrow keys step through them; the seminar log below lists every topic.</desc>
{{ gur_cells }}
{%- assign prev = -1 -%}
{%- assign stack = 0 -%}
{%- for s in seminars -%}
{%- assign ts = s.date | date: '%s' | plus: 0 -%}
{%- assign wk = ts | minus: t0 | divided_by: 604800 -%}
{%- if wk == prev -%}{%- assign stack = stack | plus: 1 -%}{%- else -%}{%- assign stack = 0 -%}{%- endif -%}
{%- assign prev = wk -%}
{%- if s.milestone -%}
{%- assign cx = wk | times: 10 | plus: 14 -%}
{%- assign ly = stack | times: 10 -%}
{%- assign ly = 53 | minus: ly -%}
<line class="gur-rule" x1="{{ cx }}" y1="17" x2="{{ cx }}" y2="{{ ly }}"/>
<text class="gur-text" x="{{ cx }}" y="12" text-anchor="{{ s.anchor | default: 'middle' }}">{{ s.milestone }}</text>
{%- endif -%}
{%- endfor -%}
{%- assign months = '2020-01-06|Jan 2020,2020-07-06|Jul 2020,2021-01-04|Jan 2021,2021-07-05|Jul 2021' | split: ',' -%}
{%- for m in months -%}
{%- assign mp = m | split: '|' -%}
{%- assign ts = mp[0] | date: '%s' | plus: 0 -%}
{%- assign mx = ts | minus: t0 | divided_by: 604800 | times: 10 | plus: 14 -%}
<line class="gur-rule" x1="{{ mx }}" y1="67" x2="{{ mx }}" y2="71"/>
<text class="gur-text-muted" x="{{ mx }}" y="81" text-anchor="middle">{{ mp[1] }}</text>
{%- endfor -%}
{%- assign anchors = 'start|middle|end' | split: '|' -%}
{%- for p in (1..3) -%}
{%- assign ps = seminars | where: 'phase', p -%}
{%- if ps.size > 0 -%}
{%- assign a = ps.first.date | date: '%s' | plus: 0 -%}
{%- assign a = a | minus: t0 | divided_by: 604800 | times: 10 | plus: 10 -%}
{%- assign b = ps.last.date | date: '%s' | plus: 0 -%}
{%- assign b = b | minus: t0 | divided_by: 604800 | times: 10 | plus: 18 -%}
{%- assign i = p | minus: 1 -%}
{%- assign anchor = anchors[i] -%}
{%- if anchor == 'start' -%}{%- assign tx = a -%}{%- elsif anchor == 'end' -%}{%- assign tx = b -%}{%- else -%}{%- assign tx = a | plus: b | divided_by: 2 -%}{%- endif -%}
<path class="gur-rule" d="M{{ a }} 90 V94 H{{ b }} V90"/>
<text class="gur-text" x="{{ tx }}" y="108" text-anchor="{{ anchor }}">{{ phase_names[i] }}</text>
<text class="gur-text-muted" x="{{ tx }}" y="121" text-anchor="{{ anchor }}">{{ ps.first.date | date: '%b %Y' }} – {{ ps.last.date | date: '%b %Y' }} · {{ ps.size }} talks</text>
{%- endif -%}
{%- endfor -%}
</svg>
<svg class="gur-tl-narrow" viewBox="0 34 850 32" preserveAspectRatio="none" role="img" tabindex="0" aria-labelledby="gur-tln-title">
<title id="gur-tln-title">Seminar timeline: {{ seminars.size }} seminars, one bar per week from December 2019 to July 2021</title>
{{ gur_cells }}
</svg>
<ol class="gur-tl-legend">
{%- for p in (1..3) -%}
{%- assign ps = seminars | where: 'phase', p -%}
{%- assign i = p | minus: 1 -%}
<li><strong>{{ phase_names[i] | replace: 'person-following', '<span class="nobr">person-following</span>' }}</strong> <span class="nobr">{{ ps.first.date | date: '%b %Y' }} – {{ ps.last.date | date: '%b %Y' }}</span> · <span class="nobr">{{ ps.size }} talks</span>
{%- for s in ps -%}{%- if s.milestone -%}{{ ' · ' }}{{ s.milestone }} <span class="nobr">({{ s.date | date: '%b %Y' }})</span>{%- endif -%}{%- endfor -%}
</li>
{%- endfor -%}
</ol>
</div>
<p class="gur-caption">One mark per seminar, one column per week. Hover, tap or tab to a mark for its topic; the full list is in the seminar log at the end.</p>

## 1 · Servo packets to <span class="nobr">a legged robot</span>

<p class="gur-caption">Dec.&nbsp;2019 – Mar.&nbsp;2020 · ATmega128, DYNAMIXEL <span class="nobr">AX-12A</span> / <span class="nobr">RX-64</span> / <span class="nobr">EX-106+</span>, <span class="nobr">RS-485</span></p>

- **Protocol by hand.** I drove DYNAMIXEL servos from a bare ATmega128. The <span class="nobr">half-duplex</span> line switching, the instruction packets and their checksums were written byte by byte. I parsed the status packets, checked them on the oscilloscope, and then moved several servos at once with Sync Write.
- **From kinematics to a walking robot.** I derived forward and inverse kinematics for a <span class="nobr">3-axis</span> arm, first as a <span class="nobr">2-D</span> problem and then with the DH convention. The same <span class="nobr">3-DOF</span> leg, on <span class="nobr">RX-64</span> and <span class="nobr">EX-106+</span> servos over <span class="nobr">RS-485</span>, became the leg of a legged "spider" robot that walks and turns.
- **Measured, then redesigned.** I traced foot positions on paper and compared them with the computed ones (<span class="nobr">2–5&nbsp;mm</span> apart). A leg that should keep its stride drifted by 25&nbsp;mm, so I replaced <span class="nobr">joint-angle</span> steps with Cartesian interpolation and inverse kinematics at every small step.

<div class="gur-media gur-media-2">
  <figure>
    <video src="{{ '/assets/video/projects/ground-up-robotics/quadruped-walk.mp4' | relative_url }}" poster="{{ '/assets/img/projects/ground-up-robotics/quadruped-walk-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="gur-caption">The legged robot walking (Mar.&nbsp;2020): <span class="nobr">3-DOF</span> legs, a <span class="nobr">hand-soldered</span> ATmega128 controller, <span class="nobr">RS-485</span> servo bus.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/ground-up-robotics/packets-on-the-scope.webp" alt="Seminar slide: DYNAMIXEL instruction and status packets on an oscilloscope, with the raw status bytes" zoomable=true %}
    <figcaption class="gur-caption">Instruction and status packets on the oscilloscope, next to the raw bytes. Error byte 0x00 means a clean exchange. Slides are in Korean; click to zoom.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/ground-up-robotics/rs485-pullup-fix.webp" alt="Seminar slide: RS-485 receive line before and after adding a pull-up resistor, with the angle readings" zoomable=true %}
    <figcaption class="gur-caption">The <span class="nobr">RS-485</span> receive line floated whenever the driver was off, and angles read back as garbage (251°, 15°, 31°). With a <span class="nobr">pull-up</span> and a termination resistor, the readings became stable.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/ground-up-robotics/leg-measured-vs-computed.webp" alt="Seminar slide: leg positions measured with a ruler and protractor, compared with the computed values" zoomable=true %}
    <figcaption class="gur-caption">Checking the kinematics on paper: computed vs. measured reach and joint angle.</figcaption>
  </figure>
</div>

## 2 · Following unit: ultrasonic ranging <span class="nobr">and my own boards</span>

<p class="gur-caption">Mar. – Nov.&nbsp;2020 · ATmega128 → STM32 (<span class="nobr">Cortex-M4</span>), ultrasonic transducers, nRF24L01+, OrCAD</p>

- **Sensors measured before they were chosen.** The robot would follow a person who carries a small transmitter. A radio message marks the moment a 40&nbsp;kHz ultrasonic burst leaves, so each receiver measures a <span class="nobr">one-way</span> time of flight, and the law of cosines turns two or three ranges into distance and bearing. I tested each candidate sensor against a tape measure. One reached 1&nbsp;cm and 1.6° in <span class="nobr">three-sensor</span> triangulation, but I still dropped it: at 70&nbsp;ms per reading and a 30° beam, it could not meet the 30&nbsp;ms target.
- **Causes, not filters.** Range spikes during fast motion survived a <span class="nobr">low-pass</span> filter, so I kept looking and found reflections. A sweep of drive voltage against acceptance angle settled on 9&nbsp;V. Once the spikes were gone, the smoothing filter came out again, because it only added lag.
- **My own boards and drivers.** I laid out two boards in OrCAD, with trace widths and vias sized for current, and wrote a <span class="nobr">26-slide</span> PCB manual along the way. I brought the boards up on the bench and wrote a <span class="nobr">register-level</span> nRF24L01+ driver, first on the ATmega128 and then on an STM32. <span class="nobr">End-to-end</span> tuning cut the trigger skew between the boards from 424 to 84&nbsp;µs and the update period from 50 to 35&nbsp;ms.

<div class="gur-media gur-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/ground-up-robotics/reception-map.webp" alt="Seminar slide: transmitter positions on a floor grid and the measured reception boundary of the receivers" zoomable=true %}
    <figcaption class="gur-caption">Mapping where the receivers still hear the transmitter: the transmitter moved point by point across a floor grid.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/ground-up-robotics/rf-latency-6ms.webp" alt="Seminar slide: RF latency measured on the oscilloscope, a table and a chart showing 6.00 to 6.02 ms from 50 to 350 cm" zoomable=true %}
    <figcaption class="gur-caption">RF latency after the fix: <span class="nobr">6.00–6.02&nbsp;ms</span> from 50 to 350&nbsp;cm, so a constant 6.01&nbsp;ms offset is enough (0.01&nbsp;ms ≈ 0.34&nbsp;cm).</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/ground-up-robotics/own-board-layouts.webp" alt="Seminar slide: two finished PCB layouts" zoomable=true %}
    <figcaption class="gur-caption">The two boards I laid out in July 2020.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/ground-up-robotics/own-board-assembled.webp" alt="Seminar slide: the assembled main board and an oscilloscope trace showing a signal offset from a damaged MCU pin" zoomable=true %}
    <figcaption class="gur-caption">The assembled main board on the bench. An offset on the scope gave away a damaged MCU pin.</figcaption>
  </figure>
</div>

## 3 · Graduation project: <span class="nobr">a person-following robot</span>

<p class="gur-caption">Dec.&nbsp;2020 – Jul.&nbsp;2021 · a team of three; my part was the following unit · STM32F429 / F405, nRF24L01+, SRF02</p>

- **The system.** The goal was a tracked transport robot for construction sites that follows a worker carrying a handheld target. My teammates handled the drive (motors and IMU) and <span class="nobr">camera-based</span> target detection. I built the following unit: the <span class="nobr">radio-synchronized</span> ultrasonic localization, its boards, and the handheld target.
- **Localization that held up under measurement.** Four receivers on a <span class="nobr">45 × 20&nbsp;cm</span> frame locate the target every 29&nbsp;ms. After I <span class="nobr">re-mounted</span> the receivers at an outward angle, the error stayed within 3.6&nbsp;cm and 2° up to 40° <span class="nobr">off-axis</span> at <span class="nobr">1–1.5&nbsp;m</span>. A lost radio acknowledgment delayed the burst by about 2.5&nbsp;ms, which is roughly 85&nbsp;cm of range error. I turned off <span class="nobr">auto-retransmit</span> and added a resend timeout and a 70&nbsp;cm jump filter, then checked the result over 519 exchanges.
- **Boards, and a dead end on record.** The <span class="nobr">following-control</span> board (STM32F429, <span class="nobr">80.8 × 74.4&nbsp;mm</span>) has four ultrasonic UARTs, four DYNAMIXEL ports, a CAN IMU, radio, Bluetooth and six infrared inputs. A 90° <span class="nobr">wide-angle</span> receiver never worked with our transmitter. I measured why (57 vs. 3.8&nbsp;Vpp drive, different attenuation) and wrote it up.

<div class="gur-media gur-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/ground-up-robotics/tracked-robot.webp" alt="Seminar slide: side and top photos of the tracked robot with the IMU and the ultrasonic sensor mast marked" zoomable=true %}
    <figcaption class="gur-caption">The tracked chassis, with the IMU and the mast for the ultrasonic receivers marked.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/ground-up-robotics/system-architecture.webp" alt="Seminar slide: system diagram of the robot (following-control and motor-control STM32 boards) and the handheld remote" zoomable=true %}
    <figcaption class="gur-caption">System architecture: my <span class="nobr">following-control</span> board, the <span class="nobr">motor-control</span> board, and the handheld target and remote.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/ground-up-robotics/rf-spike-filter.webp" alt="Seminar slide: ranging sequence and range plots before and after handling radio acknowledgment failures" zoomable=true %}
    <figcaption class="gur-caption">Range over time, before and after handling lost radio packets: the 200&nbsp;cm spikes are gone.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/ground-up-robotics/follow-board-layout.webp" alt="Seminar slide: block diagram and PCB layout of the following-control board" zoomable=true %}
    <figcaption class="gur-caption">The <span class="nobr">following-control</span> board: block diagram and layout (Jul.&nbsp;2021).</figcaption>
  </figure>
</div>

## Debugging log

Some of the faults I tracked down, and how I found them.

<div class="gur-table-wrap gur-debug">
<table>
<thead><tr><th>When</th><th>Symptom</th><th>How I found it</th><th>Fix</th></tr></thead>
<tbody>
<tr><td data-label="When">Jan.&nbsp;2020</td><td data-label="Symptom">Delays ran about 15× too long on a new controller board</td><td data-label="How I found it"><span class="nobr">Back-calculated</span> the real clock (about 1&nbsp;MHz instead of 14.7456&nbsp;MHz). Measured both crystals on the scope and checked the fuse bits.</td><td data-label="Fix">Replaced the MCU: the first chip or its soldering was bad.</td></tr>
<tr><td data-label="When">Feb.&nbsp;2020</td><td data-label="Symptom">Servo angles read back as garbage</td><td data-label="How I found it">Probed the <span class="nobr">RS-485</span> transceiver. The receive line floats whenever the driver is off.</td><td data-label="Fix">Added a 10&nbsp;kΩ <span class="nobr">pull-up</span> and a termination resistor, and confirmed with before and after captures.</td></tr>
<tr><td data-label="When">May&nbsp;2020</td><td data-label="Symptom">Range spikes during fast motion that a <span class="nobr">low-pass</span> filter could not remove</td><td data-label="How I found it">Checked the received frequency, then traced the spikes to reflections. Swept drive voltage against acceptance angle.</td><td data-label="Fix">Drove the transmitter at 9&nbsp;V and removed the filter.</td></tr>
<tr><td data-label="When">Sep.&nbsp;2020</td><td data-label="Symptom">Radio latency jittered between 9.5 and 10.5&nbsp;ms</td><td data-label="How I found it">Timed each step of the loop. Reading the status register alone took 2.73&nbsp;ms.</td><td data-label="Fix">Shortened the loop. Latency became <span class="nobr">6.00–6.02&nbsp;ms</span> and is now a constant offset.</td></tr>
<tr><td data-label="When">Jan.&nbsp;2021</td><td data-label="Symptom">The radio worked on my own board but stayed silent on a dev board</td><td data-label="How I found it">Compared SPI traffic on a logic analyzer, matched the register writes, and checked every register against the datasheet, one change at a time.</td><td data-label="Fix">The datasheet's state diagram showed CE was never raised. Driving CE fixed it.</td></tr>
<tr><td data-label="When">Feb.&nbsp;2021</td><td data-label="Symptom">A target standing still at 70&nbsp;cm sometimes read about 210&nbsp;cm</td><td data-label="How I found it">Timed the radio handshake on the scope. Each lost packet or acknowledgment delays the burst by <span class="nobr">2.5–3&nbsp;ms</span>.</td><td data-label="Fix">Turned off <span class="nobr">auto-retransmit</span> and added a resend timeout and a 70&nbsp;cm jump filter. Checked over 519 exchanges.</td></tr>
<tr><td data-label="When">May&nbsp;2021</td><td data-label="Symptom">A 90° <span class="nobr">wide-angle</span> receiver gave erratic data</td><td data-label="How I found it">Measured both transmitters (57 vs. 3.8&nbsp;Vpp) and matched echo amplitudes by distance. It worked only at <span class="nobr">25–45&nbsp;cm</span>.</td><td data-label="Fix">Recorded it as a dead end and kept the original receivers.</td></tr>
</tbody>
</table>
</div>

## Seminar log

<details class="gur-log">
<summary>All {{ seminars.size }} seminars, Dec.&nbsp;2019 – Jul.&nbsp;2021</summary>
<div class="gur-table-wrap">
<table>
<thead><tr><th>Date</th><th>Topic</th></tr></thead>
<tbody>
{%- comment -%} Words with a hyphen or a dash stay whole; a number stays on the line of its unit or arrow. {%- endcomment -%}
{%- assign units = 'ms|µs|cm|mm|m|MHz|kHz|Hz|V|Vpp|kΩ|%|Mbit/s|→' | split: '|' -%}
{%- for s in seminars -%}
<tr><td>{{ s.date | date: '%Y-%m-%d' }}</td><td>
{%- assign words = s.topic | split: ' ' -%}
{%- for w in words -%}
{%- if w contains '-' or w contains '–' -%}<span class="nobr">{{ w | escape }}</span>{%- else -%}{{ w | escape }}{%- endif -%}
{%- unless forloop.last -%}
{%- assign nw = words[forloop.index] | remove: ',' | remove: ';' | remove: ')' | remove: ':' -%}
{%- if units contains nw or w == '→' -%}&nbsp;{%- else -%}{{ ' ' }}{%- endif -%}
{%- endunless -%}
{%- endfor -%}
</td></tr>
{%- endfor -%}
</tbody>
</table>
</div>
</details>

<div class="gur-ko" lang="ko">
<p><strong>한국어 요약</strong></p>
<p>한국공학대학교 IHLAB 학부연구생 시절(<span class="nobr">2019.12–2021.07</span>)에 거의 매주 진행한 랩 세미나 {{ seminars.size }}회를 요약한 페이지입니다. ATmega128에서 다이나믹셀 패킷을 한 바이트씩 직접 만들고 오실로스코프로 확인하는 데서 시작해, 기구학으로 다리 로봇을 걷게 했습니다. 이어서 초음파와 RF 동기화로 사람의 위치를 재는 추종부를 직접 설계한 STM32 보드로 만들었고, 이 작업은 사람을 따라가는 공사장 자재 운반 로봇(졸업작품)으로 이어졌습니다.</p>
<p>모든 결과는 줄자·각도기·오실로스코프로 실측과 비교했습니다. 문제는 필터로 덮기보다 원인(반사파, 느린 레지스터 읽기, 올라가지 않은 CE 핀)을 찾아 고쳤고, 실패와 막다른 길까지 매주 기록했습니다.</p>
</div>

<script>
  // Timeline tooltip: the nearest square within 24px on hover or tap; arrow keys when a chart has focus.
  (function () {
    var root = document.getElementById("gur-timeline");
    if (!root) return;
    var tip = document.createElement("div");
    var tipDate = document.createElement("div");
    var tipText = document.createElement("div");
    tip.className = "gur-tip";
    tipDate.className = "gur-tip-date";
    tip.hidden = true;
    tip.appendChild(tipDate);
    tip.appendChild(tipText);
    document.body.appendChild(tip);
    var activeCell = null;

    function hide() {
      if (activeCell) activeCell.classList.remove("is-active");
      activeCell = null;
      tip.hidden = true;
    }

    function show(cell) {
      if (activeCell) activeCell.classList.remove("is-active");
      activeCell = cell;
      cell.classList.add("is-active");
      tipDate.textContent = cell.getAttribute("data-date");
      // No line break inside "2-D" or "6.01 ms": non-breaking hyphens and spaces.
      tipText.textContent = cell
        .getAttribute("data-topic")
        .replace(/(\w)-(?=\w)/g, "$1\u2011")
        .replace(/(\d) (?=(ms|µs|cm|mm|m|MHz|kHz|Hz|Vpp|V|kΩ|%|→)(?![A-Za-z]))/g, "$1\u00a0")
        .replace(/ → /g, "\u00a0→\u00a0");
      tip.hidden = false;
      var r = cell.getBoundingClientRect();
      var w = tip.offsetWidth;
      var h = tip.offsetHeight;
      var x = Math.min(Math.max(8, r.left + r.width / 2 - w / 2), window.innerWidth - w - 8);
      var y = r.top - h - 8;
      if (y < 8) y = r.bottom + 8;
      tip.style.left = x + "px";
      tip.style.top = y + "px";
    }

    Array.prototype.forEach.call(root.querySelectorAll("svg"), function (svg) {
      var cells = Array.prototype.slice.call(svg.querySelectorAll(".gur-cell"));
      function nearest(e) {
        var best = null;
        var bestD = 24 * 24;
        for (var i = 0; i < cells.length; i++) {
          var r = cells[i].getBoundingClientRect();
          var dx = e.clientX - (r.left + r.width / 2);
          var dy = e.clientY - (r.top + r.height / 2);
          var d = dx * dx + dy * dy;
          if (d < bestD) {
            bestD = d;
            best = cells[i];
          }
        }
        if (!best) hide();
        else if (best !== activeCell) show(best);
      }
      svg.addEventListener("pointermove", nearest);
      svg.addEventListener("pointerdown", nearest);
      svg.addEventListener("pointerleave", function (e) {
        if (e.pointerType === "mouse") hide();
      });
      svg.addEventListener("blur", hide);
      svg.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
          e.preventDefault();
          var i = cells.indexOf(activeCell);
          i = i < 0 ? 0 : i + (e.key === "ArrowRight" ? 1 : -1);
          show(cells[Math.max(0, Math.min(cells.length - 1, i))]);
        } else if (e.key === "Escape") {
          hide();
        }
      });
    });
    window.addEventListener("scroll", hide, { passive: true });
  })();
</script>
