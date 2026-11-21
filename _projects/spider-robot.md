---
layout: page
title: Legged Robot from Raw Servo Packets
description: "Winter project, Dec. 2019 –⁠ Mar. 2020: a legged robot on DYNAMIXEL servos, packets and kinematics worked out by hand"
img: assets/img/projects/spider-robot/thumb.webp
importance: 2
---

<!-- Session data: _data/ihlab_seminars.yml, project 'spider' (14 seminars, 2019-12-31 – 2020-03-19). Styles: "Project pages" in _sass/_custom.scss. -->
{%- assign sessions = site.data.ihlab_seminars | where: 'project', 'spider' -%}

From Dec.&nbsp;2019 to Mar.&nbsp;2020, as an undergraduate researcher at IHLAB (Tech University of Korea), I worked on a legged “spider” robot driven by DYNAMIXEL servos as my winter project. Starting from an ATmega128 training board, I wrote the servo protocol byte by byte, worked out the kinematics for a <span class="nobr">3-axis</span> arm and then for the legs, and debugged the servo bus on an oscilloscope. The first goal in my December plan was a <span class="nobr">four-legged</span> spider robot; by March it crawled and turned on three legs and a caster, open loop. The legs, the suction feet and the green controller PCB were the lab’s; the firmware, the kinematics, a <span class="nobr">half-duplex</span> adapter, the <span class="nobr">RS-485</span> fixes and the final <span class="nobr">hand-wired</span> controller are mine.

<div class="prj-stats">
  <div class="prj-stat"><span class="prj-stat-value">{{ sessions.size }}</span><span class="prj-stat-label">lab seminars in 12&nbsp;weeks</span></div>
  <div class="prj-stat"><span class="prj-stat-value">318</span><span class="prj-stat-label">status packets in a raw log, 0&nbsp;checksum failures</span></div>
  <div class="prj-stat"><span class="prj-stat-value">0.56<span class="prj-unit">°</span></span><span class="prj-stat-label">largest gap between commanded and <span class="nobr">read-back</span> arm&nbsp;angles</span></div>
  <div class="prj-stat"><span class="prj-stat-value">2<span class="prj-unit">mm</span></span><span class="prj-stat-label">largest foot error traced on paper after the redesign, down from 25&nbsp;mm</span></div>
</div>

## What this project shows

<div class="prj-traits">
  <div class="prj-trait">
    <strong>Protocol from the wire up</strong>
    <p>I wrote the DYNAMIXEL packets and checksums byte by byte in C, with no servo library, after soldering the <span class="nobr">half-duplex</span> adapter they needed. A raw log of 318 status packets has 0 checksum&nbsp;failures.</p>
  </div>
  <div class="prj-trait">
    <strong>Measured against ground truth</strong>
    <p>I measured leg poses with a ruler and traced foot paths on paper, before and after the redesign: the largest traced error fell from 25 to 2&nbsp;mm. In December I had already checked servo goal positions against a&nbsp;protractor.</p>
  </div>
  <div class="prj-trait">
    <strong>Root causes, found on the scope</strong>
    <p>A clock 15× too slow, a leg that glitched, angles that read 4016.192°: I traced each to its cause with the oscilloscope (a faulty MCU or its soldering, status replies colliding with commands, a floating receive line) and fixed that&nbsp;cause.</p>
  </div>
  <div class="prj-trait">
    <strong>Dead ends on record</strong>
    <p>My talk of 30&nbsp;Jan.&nbsp;2020 lists the leg glitch’s cause as “not found”; the next talk found it. The final runs were open loop because <span class="nobr">present-angle</span> reads kept failing, and the March talk says&nbsp;so.</p>
  </div>
</div>

## Timeline

{% include prj_timeline.liquid sessions=sessions start='2019-12-30' weeks=12 ticks='2020-01-06|Jan 2020,2020-02-03|Feb 2020,2020-03-02|Mar 2020' parts='arm|Robot arm,leg|Legged robot' noun='seminars' %}
<p class="prj-caption">One mark per seminar, one column per week. Hover, tap or tab to a mark for its topic; the full list is in the log at the&nbsp;end.</p>

## The robot, March&nbsp;2020

- **Three legs and a caster.** Each leg has three joints: an <span class="nobr">EX-106+</span> hip, turned through a 2:1 belt, and two <span class="nobr">RX-64</span> servos, on an <span class="nobr">RS-485</span> bus at about 14&nbsp;V. The final runs used three legs and a caster, and with the caster in place all legs could move at the same time.
- **Open loop, said plainly.** In March, <span class="nobr">present-angle</span> reads failed so often that I ran the robot without them, on commanded positions alone. The serial command interface, laid out in February, was 1 for forward, 2 for turn right and 3 for turn left.
- **My own controller, wired by hand.** I rebuilt the controller on perfboard: an ATmega128 core module, a buck converter module, a Bluetooth module, a MAX485 <span class="nobr">RS-485</span> transceiver and four servo connectors, wired point to point underneath.
- **A bad wire, found by elimination.** Only leg&nbsp;C moved jerkily, so I ruled out the code. A multimeter check of the circuit’s wiring found no fault and no short, so I concluded the wire itself was bad; after I replaced it, leg&nbsp;C moved smoothly.

<div class="prj-media prj-media-2">
  <figure>
    <video src="{{ '/assets/video/projects/spider-robot/walk-oblique-2020-03.mp4' | relative_url }}" poster="{{ '/assets/img/projects/spider-robot/walk-oblique-2020-03-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">12&nbsp;Mar.&nbsp;2020: the robot crawls on three legs and a caster, open loop, with my <span class="nobr">hand-wired</span> controller on&nbsp;top.</figcaption>
  </figure>
  <figure>
    <video src="{{ '/assets/video/projects/spider-robot/turn-topdown-2020-03.mp4' | relative_url }}" poster="{{ '/assets/img/projects/spider-robot/turn-topdown-2020-03-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">The final run on 17&nbsp;Mar.&nbsp;2020, seen from above: the robot turns. The fourth corner holds a bare hip bracket, not a&nbsp;leg.</figcaption>
  </figure>
</div>

<div class="prj-media">
  <figure>
    {% include figure.liquid path="assets/img/projects/spider-robot/perfboard-controller-2020-03.webp" alt="Hand-wired perfboard controller, top side mounted on the robot and the underside wiring: ATmega128 core module, buck converter module, Bluetooth module, MAX485 transceiver and servo connectors" zoomable=true %}
    <figcaption class="prj-caption">My <span class="nobr">hand-wired</span> controller (Mar.&nbsp;2020), top and underside: ATmega128 core module, buck module, Bluetooth module, MAX485 and four servo connectors, wired point to&nbsp;point.</figcaption>
  </figure>
</div>

## Servo protocol, byte by byte

- **A <span class="nobr">half-duplex</span> adapter first.** The <span class="nobr">AX-12A</span> sends and receives on one data line, so in December I soldered an adapter for it: a buffer IC on an SOIC breakout board, a 10&nbsp;kΩ <span class="nobr">pull-up</span> and a servo connector, with two port pins switching the direction.
- **Packets checked against a protractor.** I built each instruction packet and its checksum, <code class="nobr">~(ID + LEN + INST + params)</code>, by hand. Goal positions 0x0300, 0x0200 and 0x0100 should turn the horn to 225°, 150° and 75°, and I photographed each one against a protractor.
- **Replies logged raw.** I checked the status packets on the oscilloscope and logged the raw bytes: 318 packets, every checksum valid. Then came Sync Write, one broadcast packet for several servos with no reply, and a mirror demo in which one servo’s present angle became another’s goal.
- **From one servo to a <span class="nobr">3-axis</span> arm.** I solved the arm’s <span class="nobr">2-D</span> inverse kinematics with the law of cosines, fixing one angle to remove the redundancy of three joints. Commanded angles of 150, 145.681 and 183.683° read back as 149.723, 145.621 and 183.125°: within 0.56°, less than two steps of the servo’s 0.293° resolution.

<div class="prj-media">
  <figure>
    {% include figure.liquid path="assets/img/projects/spider-robot/protractor-check-2019-12.webp" alt="Three photos of an AX-12A servo horn against a protractor at goal positions 0x0300, 0x0200 and 0x0100, with the instruction-packet code and the angle arithmetic under each" zoomable=true %}
    <figcaption class="prj-caption">Goals 0x0300, 0x0200 and 0x0100 against a protractor: 225°, the 150° center and 75° (Dec.&nbsp;2019). Slides are in Korean; click to&nbsp;zoom.</figcaption>
  </figure>
</div>

<div class="prj-media prj-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/spider-robot/half-duplex-adapter-2019-12.webp" alt="Hand-soldered half-duplex adapter on an SOIC breakout board, front and back: buffer IC, 10 kilohm pull-up resistor, three-pin servo connector and point-to-point wiring" zoomable=true %}
    <figcaption class="prj-caption">The <span class="nobr">half-duplex</span> adapter I soldered (Dec.&nbsp;2019), front and back: buffer IC, 10&nbsp;kΩ <span class="nobr">pull-up</span>, servo&nbsp;connector.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/spider-robot/status-packets-scope-2020-01.webp" alt="Seminar slide: oscilloscope captures of an instruction packet and a status packet, and a serial log of status packets with error byte 00" zoomable=true %}
    <figcaption class="prj-caption">Instruction and status packets on the scope, and the first logged replies, error byte 0x00. The full raw log holds 318 status packets with 0 checksum failures (Jan.&nbsp;2020).</figcaption>
  </figure>
</div>

## Faults found on the oscilloscope

- **The lab’s board, populated by me.** The 140&nbsp;×&nbsp;90&nbsp;mm controller PCB was the lab’s. I populated it with the ATmega128 and a MAX485 transceiver, added a buck converter on a perfboard daughterboard and wired in the 14&nbsp;V supply. When 14&nbsp;V later reached the MCU and destroyed it, I soldered the circuit again with only the parts in use, to avoid shorts.
- **A clock 15× too slow.** On that board, `delay_us(10)` took 150&nbsp;µs. From the delay loop’s cycle count I estimated a clock of about 1&nbsp;MHz instead of 14.7456&nbsp;MHz. I <span class="nobr">re-soldered</span> the crystal, <span class="nobr">re-set</span> the fuse bits and probed both crystal pins; the crystal oscillated near its nominal frequency, so I replaced the MCU, and `delay_us(10)` then took 10.0&nbsp;µs.
- **Replies colliding with commands.** The first leg glitched now and then, and my talk of 30&nbsp;Jan. listed the cause as not found. On the scope, each servo answers a write with a status reply, about 700&nbsp;µs later by the slide’s note, while my code sent the next command after only 100&nbsp;µs. Setting Status Return Level&nbsp;2&nbsp;→&nbsp;1, so that servos answer only reads, stopped the glitches.
- **<span class="nobr">RS-485</span> at the physical layer.** On transmit, my code released the driver enable as soon as the transmit buffer was empty, before the last byte had left; the fix waits 200&nbsp;µs before releasing it, with interrupts off. On receive, the MCU’s RX line floats while the MAX485 transmits, because its receiver is disabled then, and angles read 4016.192° or random values. A 10&nbsp;kΩ <span class="nobr">pull-up</span> on that line made the readings follow the command (13.425°&nbsp;↔&nbsp;60.748°); I also added a termination resistor across A and B against reflections.

<div class="prj-media">
  <figure>
    {% include figure.liquid path="assets/img/projects/spider-robot/clock-fault-before-after-2020-01.webp" alt="Two oscilloscope screenshots: edges 150 microseconds apart on 23 January 2020, and a square wave with 10.0 microsecond steps on 29 January 2020" zoomable=true %}
    <figcaption class="prj-caption">The slow clock on the scope: <code>delay_us(10)</code> took 150&nbsp;µs on 23&nbsp;Jan.&nbsp;2020 (left) and 10.0&nbsp;µs on 29&nbsp;Jan., after the MCU was replaced&nbsp;(right).</figcaption>
  </figure>
</div>

<div class="prj-media prj-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/spider-robot/lab-board-populated-2020-01.webp" alt="The lab's green controller PCB populated with an ATmega128 and a MAX485, with a perfboard buck-converter daughterboard and a red 14 V lead" zoomable=true %}
    <figcaption class="prj-caption">The lab’s controller PCB as I populated it (Jan.&nbsp;2020), with my buck daughterboard and the red 14&nbsp;V lead. The board design is the lab’s, not&nbsp;mine.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/spider-robot/status-reply-collision-2020-02.webp" alt="Seminar slide: oscilloscope photo of a command followed by a servo's status reply, the 100 microsecond delay in the code, and Status Return Level changed from 2 to 1" zoomable=true %}
    <figcaption class="prj-caption">Each write draws a status reply (about 700&nbsp;µs later, by the slide’s note), but the next command left after 100&nbsp;µs. Status Return Level&nbsp;2&nbsp;→&nbsp;1 fixed&nbsp;it.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/spider-robot/rs485-transmit-fix-2020-02.webp" alt="Seminar slide: oscilloscope captures of RS-485 packets with their ends marked, and the transmit code before and after moving the driver-enable release" zoomable=true %}
    <figcaption class="prj-caption"><span class="nobr">RS-485</span> transmit: the driver enable was released before the last byte had left (marked on the capture of 13&nbsp;Feb.&nbsp;2020). The fix releases it 200&nbsp;µs&nbsp;later.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/spider-robot/rs485-receive-fix-2020-02.webp" alt="Seminar slide: RS-485 receive line before and after a pull-up resistor, with random angle readings before and readings that follow the command after" zoomable=true %}
    <figcaption class="prj-caption"><span class="nobr">RS-485</span> receive, before and after the <span class="nobr">pull-up</span>: random angles (251.207°, 15.631°, 31.386°), then readings that follow the command (13.425°&nbsp;↔&nbsp;60.748°).</figcaption>
  </figure>
</div>

## Kinematics, checked on paper

- **Joints that finish together.** For each move the firmware read the present angles, set each joint’s speed in proportion to the angle it still had to turn, queued the three goals with REG_WRITE and started them with a single ACTION, so that all three joints would finish together.
- **A drift found, and its cause.** A ruler confirmed single poses (147 against 150&nbsp;mm, 70 against 69&nbsp;mm), but during moves the foot that should have stayed 150&nbsp;mm from the body traced 145 and 125&nbsp;mm. Splitting a move by joint angles cannot hold a Cartesian distance, so I rewrote it: forward kinematics gives the current point, small Cartesian steps lead to the target, and inverse kinematics runs at every step.
- **A conversion bug, found by plotting.** I logged x, y and z at every step and plotted them. In one step x jumped from 180 to 208.074 and y from 84 to 105.588, which pointed to a wrong conversion; after the fix, x held near 180&nbsp;mm while y and z traced clean trapezoids.
- **<span class="nobr">Re-traced</span> after the redesign.** The foot then kept 179 and 178.5&nbsp;mm against a target of 180, the hip turned 29.7° against 30°, and the sideways reach was 234 and 123&nbsp;mm against 235 and 125: every trace within <span class="nobr">1–2&nbsp;mm</span> and 0.3°.

<div class="prj-media prj-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/spider-robot/foot-trace-before-2020-02.webp" alt="Seminar slide: leg motions traced on paper with distances and a protractor, and tables of computed versus measured values" zoomable=true %}
    <figcaption class="prj-caption">Paper traces on 18&nbsp;Feb.&nbsp;2020: reach within <span class="nobr">2–5&nbsp;mm</span> and the hip within 2°, but the lateral distance meant to stay at 150&nbsp;mm read 145 and 125&nbsp;mm.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/spider-robot/foot-trace-after-2020-03.webp" alt="Seminar slide: foot paths re-traced on paper after the redesign, marked 179, 178.5, 234 and 123 millimeters and 29.7 degrees next to the target constants" zoomable=true %}
    <figcaption class="prj-caption"><span class="nobr">Re-traced</span> on 5&nbsp;Mar.&nbsp;2020, after the switch to Cartesian interpolation: 179 and 178.5&nbsp;mm against 180, 29.7° against 30°, 234 and 123&nbsp;mm against 235 and&nbsp;125.</figcaption>
  </figure>
</div>

<div class="prj-media">
  <figure>
    {% include figure.liquid path="assets/img/projects/spider-robot/kinematics-log-jump-and-fix-2020-02.webp" alt="Logged foot coordinates and two charts: x and y jumping as the raised leg swings forward, and after the fix, clean trapezoids for one leg's four motions" zoomable=true %}
    <figcaption class="prj-caption">Left: the logged coordinates jump as the raised leg starts its forward swing. Right: after the conversion fix, one leg’s four motions trace clean trapezoids (25&nbsp;Feb.&nbsp;2020).</figcaption>
  </figure>
</div>

## Debugging log

The faults I tracked down in these twelve weeks, and how I found&nbsp;them.

<div class="prj-table-wrap prj-debug"><table><thead><tr><th>When</th><th>Symptom</th><th>How I found it</th><th>Fix</th></tr></thead><tbody>
<tr><td data-label="When">Jan.&nbsp;2020</td><td data-label="Symptom"><code>delay_us(10)</code> took 150&nbsp;µs: the clock ran about 15× too&nbsp;slow</td><td data-label="How I found it">Estimated about 1&nbsp;MHz instead of 14.7456&nbsp;MHz from the delay loop’s cycle count. <span class="nobr">Re-soldered</span> the crystal, <span class="nobr">re-set</span> the fuse bits and probed both crystal pins: it&nbsp;oscillated.</td><td data-label="Fix">Replaced the MCU; <code>delay_us(10)</code> then took 10.0&nbsp;µs.</td></tr>
<tr><td data-label="When">Feb.&nbsp;2020</td><td data-label="Symptom">The first leg glitched now and then; my 30&nbsp;Jan. talk listed the cause as not&nbsp;found</td><td data-label="How I found it">On the scope, every write draws a status reply (about 700&nbsp;µs later, by the slide’s note), and the next command left after only 100&nbsp;µs</td><td data-label="Fix">Status Return Level&nbsp;2&nbsp;→&nbsp;1, so that servos answer reads&nbsp;only</td></tr>
<tr><td data-label="When">Feb.&nbsp;2020</td><td data-label="Symptom">The ends of <span class="nobr">RS-485</span> packets were cut&nbsp;off</td><td data-label="How I found it">Compared the capture with the code: the driver enable was released when the transmit buffer emptied, while the last byte was still being&nbsp;sent</td><td data-label="Fix">Released it 200&nbsp;µs later, with interrupts&nbsp;off</td></tr>
<tr><td data-label="When">Feb.&nbsp;2020</td><td data-label="Symptom">Angles read 4016.192° or random&nbsp;values</td><td data-label="How I found it">Probed the MAX485: the MCU’s RX line floats while the transceiver&nbsp;transmits</td><td data-label="Fix">A 10&nbsp;kΩ <span class="nobr">pull-up</span> on RX, plus a termination resistor; readings then followed the&nbsp;command</td></tr>
<tr><td data-label="When">Feb.&nbsp;2020</td><td data-label="Symptom">The foot drifted to 125&nbsp;mm from the body against a target of&nbsp;150</td><td data-label="How I found it">Traced the motion on paper: splitting a move by joint angles cannot hold a Cartesian&nbsp;distance</td><td data-label="Fix">Cartesian interpolation with inverse kinematics at every step; <span class="nobr">re-traced</span> within 2&nbsp;mm in&nbsp;March</td></tr>
<tr><td data-label="When">Feb.&nbsp;2020</td><td data-label="Symptom">Logged foot coordinates jumped at each phase&nbsp;change</td><td data-label="How I found it">Plotted x, y and z over time in a&nbsp;spreadsheet</td><td data-label="Fix">Corrected the coordinate conversion; the plots became clean&nbsp;trapezoids</td></tr>
<tr><td data-label="When">Mar.&nbsp;2020</td><td data-label="Symptom">Only leg&nbsp;C moved&nbsp;jerkily</td><td data-label="How I found it">Only one leg, so not the code; a multimeter check of the wiring found no fault or&nbsp;short</td><td data-label="Fix">Replaced the wire; leg&nbsp;C moved&nbsp;smoothly</td></tr>
</tbody></table></div>

## Seminar log

{% capture log_summary %}All {{ sessions.size }} seminars, <span class="nobr">Dec.&nbsp;2019 – Mar.&nbsp;2020</span>{% endcapture %}
{% include prj_log.liquid sessions=sessions summary=log_summary %}

<div class="prj-ko" lang="ko">
<p><strong>한국어 요약</strong></p>
<p>IHLAB 학부연구생으로 2019년&nbsp;12월부터 2020년&nbsp;3월까지 진행한 겨울방학 프로젝트입니다. ATmega128에서 다이나믹셀 패킷과 체크섬을 한 바이트씩 직접 짜고, 3축 로봇팔과 다리의 기구학을 풀었습니다. 12월 계획의 첫 목표는 다리 4개짜리 거미로봇이었고, 3월에는 다리 3개와 캐스터로 기어가며 방향을 트는 로봇을 개루프로 구동했습니다. 다리와 흡착 발, 초록색 제어 PCB는 연구실 장비이고, 펌웨어와 기구학 계산, 반이중 어댑터, <span class="nobr">RS-485</span> 통신 수정, 만능기판 제어기는 제&nbsp;작업입니다.</p>
<p>결과는 각도기와 자, 오실로스코프로 직접 재어 확인했습니다. 15배 느린 클럭은 MCU 교체로, 다리 오작동은 상태 패킷 충돌을 찾아 반환 레벨 변경으로, 엉뚱한 각도값은 풀업 저항과 종단 저항을 달아 고쳤습니다. 관절각을 나눠 움직일 때 25&nbsp;mm까지 벌어지던 발 위치 오차는 직교좌표 보간 뒤 <span class="nobr">1–2&nbsp;mm</span> 이내로 줄었고, 마지막 구동이 현재 각도를 읽지 못한 개루프였다는 점도 그대로&nbsp;기록했습니다.</p>
</div>

{% include prj_more.liquid %}
