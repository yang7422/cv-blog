---
layout: page
title: Synchronized Twin Linear Rails
description: "Two belt rails, two ATmega128s: PID position control, a GPIO handshake, homing and fault recovery, Aug. 2020 –⁠ Feb. 2021"
img: assets/img/projects/linear-rail-sync/thumb.webp
importance: 3
---

<!-- Session data: _data/ihlab_seminars.yml, entries with project 'rails'. Styles: "Project pages" in _sass/_custom.scss. Every number on this page is sourced in claims.tsv of the page build (deck :: slide, image or video + time). -->

{%- assign sessions = site.data.ihlab_seminars | where: 'project', 'rails' -%}

From Aug.&nbsp;2020 to Feb.&nbsp;2021, as an undergraduate researcher at IHLAB (Tech University of Korea), I developed the control for two <span class="nobr">belt-driven</span> linear rails that had to move together. Each rail has its own DC gearmotor with an encoder and its own ATmega128, and the motors run on bought <span class="nobr">H-bridge</span> drivers, so the two controllers have to coordinate over the wires between them. I tuned PID position control on one rail first, then took the pair through seven steps, from a scheme that did not synchronize to homing and fault recovery. Each step below is taken from a dated progress report of that period.

<div class="prj-stats">
  <div class="prj-stat"><span class="prj-stat-value">{{ sessions.size }}</span><span class="prj-stat-label">progress reports, <span class="nobr">Aug.&nbsp;2020 – Feb.&nbsp;2021</span></span></div>
  <div class="prj-stat"><span class="prj-stat-value">7</span><span class="prj-stat-label">steps from a scheme that did not synchronize to homing and fault&nbsp;recovery</span></div>
  <div class="prj-stat"><span class="prj-stat-value">99.794<span class="prj-unit">mm</span></span><span class="prj-stat-label">for a 100&nbsp;mm target, PID on one&nbsp;rail</span></div>
  <div class="prj-stat"><span class="prj-stat-value">18.07<span class="prj-unit">kHz</span></span><span class="prj-stat-label">PWM on the scope, under the new driver's 20&nbsp;kHz&nbsp;limit</span></div>
</div>

## What this project shows

<div class="prj-traits">
  <div class="prj-trait">
    <strong>Measured, not assumed</strong>
    <p>I read the PID dt off the scope, 5.65&nbsp;ms between pulses on a pin set once per loop, and counted 12141 encoder counts over the full 520&nbsp;mm stroke. On the scope the PWM read 28.90&nbsp;kHz, over a new driver's 20&nbsp;kHz limit, until a timer change brought it to 18.07&nbsp;kHz.</p>
  </div>
  <div class="prj-trait">
    <strong>The cause before the gain</strong>
    <p>When the two rails stuttered, a lower gain only traded stutter for speed (Kp&nbsp;200 against Kp&nbsp;30). The log pointed to the handshake instead: the <span class="nobr">in-position</span> window had to take in an error of 17.418&nbsp;mm, or each rail slowed before every handover. A window of 0.6&nbsp;×&nbsp;the segment (18&nbsp;mm) made the motion&nbsp;continuous.</p>
  </div>
  <div class="prj-trait">
    <strong>Dead ends on record</strong>
    <p>Streaming the master's position did not synchronize the rails, a UART lockstep stuttered, and a stop check on unchanged position was rejected (marked ✗ in its report). Each one stays in the reports next to what replaced&nbsp;it.</p>
  </div>
  <div class="prj-trait">
    <strong>Safety in the wiring</strong>
    <p><span class="nobr">Cross-wired</span> GPIO lines between the two MCUs carry "in position" and "stop", and a limit switch on a <span class="nobr">pulled-up</span> input homes each rail. On a fault both rails stop, wait 1&nbsp;s and back off toward their limit&nbsp;switches.</p>
  </div>
</div>

## Timeline

{% include prj_timeline.liquid sessions=sessions start='2020-08-17' weeks=25 ticks='2020-09-07|Sep 2020,2020-10-05|Oct 2020,2020-11-02|Nov 2020,2020-12-07|Dec 2020,2021-01-04|Jan 2021' parts='single|Single axis,sync|Two rails in sync' noun='sessions' %}

<p class="prj-caption">One mark per progress report, one column per week. Hover, tap or tab to a mark for its topic; the full list is in the log at the&nbsp;end.</p>

## 1&nbsp;· One rail first: <span class="nobr">PID position control</span>

<p class="prj-caption"><span class="nobr">Aug. – Sep.&nbsp;2020</span>&nbsp;· ATmega128, L298N <span class="nobr">H-bridge</span> module, 12&nbsp;V encoder gearmotors, a 520&nbsp;mm belt&nbsp;rail</p>

- **Drive and sense.** In Aug.&nbsp;2020 I drove a 12&nbsp;V encoder gearmotor through an L298N <span class="nobr">H-bridge</span> module with timer PWM and counted its <span class="nobr">hall-encoder</span> pulses on an external interrupt. Tuning PID angle control one gain at a time brought the peak from 216° down to 180.78° for a 180° target.
- **One belt rail under PID.** On a 520&nbsp;mm belt rail I counted 12141 encoder counts over the full stroke (0.04283&nbsp;mm per count) and pulsed a spare pin once per pass of the control loop: the scope cursors read 5.65&nbsp;ms between pulses, which became the PID dt. Sweeping P, PD, PI and PID gains one at a time, Kp&nbsp;7, Ki&nbsp;0.1 and Kd&nbsp;0.7 came closest: 99.794&nbsp;mm for a 100&nbsp;mm target.
- **The scope before a guess.** When a bench gearmotor ran slowly at 60% PWM, I put the signal on the scope with and without a capacitor. Without it the rising edges smeared; with it connected, the motor ran fast.

<div class="prj-media">
  <figure>
    {% include figure.liquid path="assets/img/projects/linear-rail-sync/pid-ki-sweep.webp" alt="Two charts of rail position, error, target and PWM command against time for Kp 7 and Kd 0.7: with Ki 1 the position settles above 100 mm, with Ki 0.1 it settles at 99.794 mm" zoomable=true %}
    <figcaption class="prj-caption">One rail, Kp&nbsp;7 and Kd&nbsp;0.7: with Ki&nbsp;1 the position (blue) settles above the 100&nbsp;mm target, with Ki&nbsp;0.1 at 99.794&nbsp;mm. Slides are in Korean; click to&nbsp;zoom.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/linear-rail-sync/pwm-capacitor.webp" alt="Two oscilloscope photos of the same PWM signal: clean square edges with the capacitor connected, jittery, smeared rising edges without it" zoomable=true %}
    <figcaption class="prj-caption">The same 60% PWM (OCR0&nbsp;153) to a bench gearmotor, with the capacitor connected (left) and without it (right), 21&nbsp;Sep.&nbsp;2020.</figcaption>
  </figure>
</div>

## 2&nbsp;· Two rails: <span class="nobr">from streaming to a hardware handshake</span>

<p class="prj-caption"><span class="nobr">Nov.&nbsp;2020 – Jan.&nbsp;2021</span>&nbsp;· <span class="nobr">steps 1–5</span>&nbsp;· one ATmega128 per rail, 24&nbsp;V encoder gearmotors, bought <span class="nobr">H-bridge</span>&nbsp;drivers</p>

- **<span class="nobr">Steps 1–2:</span> stream, then share a trajectory.** In Nov.&nbsp;2020 each rail got a 24&nbsp;V gearmotor with a <span class="nobr">512-pulse</span> encoder (0.002447&nbsp;mm per count), a bought 20&nbsp;A <span class="nobr">H-bridge</span> board and its own ATmega128. Streaming the master's position to the slave did not synchronize the rails, so both controllers instead cut the move into segments of one shared trajectory and stepped the setpoint every 10&nbsp;ms.
- **Step 3: a UART lockstep that stuttered.** At a fixed interval each MCU sent "@" (segment reached) or "/" (not yet), and neither moved on until both had arrived. The rails stuttered and crawled. A speed sketch in the report gives the cause: waiting for the other side's confirmation made each rail ramp down to a stop at every segment target and back up again.
- **Step 4: a GPIO handshake with the right window.** I moved the "in position" signal to a dedicated GPIO line, modeled on the <span class="nobr">in-position</span> (INP) output of servo drives, with a ±0.1&nbsp;mm window, but the rails still stuttered at Kp&nbsp;200, and Kp&nbsp;30 was smooth but slower. The log put a number on the problem: the window had to take in an error of 17.418&nbsp;mm, or each rail slowed before every handover. A window of 0.6&nbsp;×&nbsp;the segment length (18&nbsp;mm for 30&nbsp;mm segments) covers it, so the handover comes while the drive is still at full command, and the motion became continuous.
- **Step 5: stop on a speed drop, and stop both.** A stop check on unchanged position was rejected; the report marks it ✗. Instead I estimated speed every 10&nbsp;ms in a timer interrupt: a 300&nbsp;mm move cruised near 0.19&nbsp;m/s and ended at 300.122&nbsp;mm. A rail that slows under load after reaching cruise now cuts its PWM and raises a stop line wired to the other MCU, which stops as well.

<div class="prj-media prj-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/linear-rail-sync/kp-200-vs-30.webp" alt="Two logged charts of position, error, target and PWM command for a 300 mm move in 500 segments: with Kp 200 the PWM command jumps between 0 and its maximum; with Kp 30 it is smooth but the position rises more slowly" zoomable=true %}
    <figcaption class="prj-caption">A 300&nbsp;mm move in 500 segments under the handshake. Kp&nbsp;200 (top): the PWM command (OCR, yellow) jumps between 0 and its maximum throughout the move. Kp&nbsp;30 (bottom): smooth, but&nbsp;slower.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/linear-rail-sync/inposition-window.webp" alt="Two logged charts for Kp 15 and a 300 mm move in 10 segments: before the window fix the PWM command dips at every segment, with a tooltip marking an error of 17.418; after it the command stays at maximum and the position rises in a straight line" zoomable=true %}
    <figcaption class="prj-caption">Kp&nbsp;15, 300&nbsp;mm in 10 segments. Top, before the fix: the command (yellow) dips at every segment as the rail slows for the handover; the tooltip marks the 17.418&nbsp;mm error. Bottom, with the 18&nbsp;mm window: the command stays at maximum and the position (blue) climbs in a straight&nbsp;line.</figcaption>
  </figure>
  <figure>
    <video src="{{ '/assets/video/projects/linear-rail-sync/lockstep-hand-test.mp4' | relative_url }}" poster="{{ '/assets/img/projects/linear-rail-sync/lockstep-hand-test-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">Nov.&nbsp;2020, UART lockstep: a hand holds one carriage back, and the free one keeps pace with it instead of running&nbsp;ahead.</figcaption>
  </figure>
  <figure>
    <video src="{{ '/assets/video/projects/linear-rail-sync/cross-stop-test.mp4' | relative_url }}" poster="{{ '/assets/img/projects/linear-rail-sync/cross-stop-test-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">Jan.&nbsp;2021, <span class="nobr">cross-stop</span> test: a hand holds one carriage back, and both rails&nbsp;stop.</figcaption>
  </figure>
</div>

## 3&nbsp;· Speed in m/s, <span class="nobr">PWM under the driver's limit</span>

<p class="prj-caption">Jan.&nbsp;2021&nbsp;· step&nbsp;6&nbsp;· speed calibration, oscilloscope, Timer0 fast&nbsp;PWM</p>

- **Step 6: a drive command with units.** I measured the rail's speed at 16 PWM settings (<span class="nobr">OCR&nbsp;10–160</span>) and fitted a line, <span class="nobr">speed = 0.0036&nbsp;× duty − 0.0115</span>, with duty in % and speed in m/s. The position error could then be issued as a speed: <span class="nobr">OCR = (err + 0.0115) / 0.0036 × 2.55</span>.
- **PWM <span class="nobr">re-timed</span> for a new driver.** To match the two motors, I planned a new <span class="nobr">H-bridge</span> driver. Its datasheet allows PWM up to 20&nbsp;kHz, but my <span class="nobr">phase-correct</span> PWM read 28.90&nbsp;kHz on the scope. Switching Timer0 to fast PWM, with the counter reloaded to 155 in the overflow interrupt, brought it to 18.07&nbsp;kHz on the scope's frequency counter.

<div class="prj-media">
  <figure>
    {% include figure.liquid path="assets/img/projects/linear-rail-sync/speed-plateau.webp" alt="Chart of one rail's estimated speed against log sample: a ramp up, a plateau near 0.19 to 0.20 m/s and a ramp down" zoomable=true %}
    <figcaption class="prj-caption">Speed of one rail, estimated every 10&nbsp;ms during a move (m/s against log sample): a ramp up, a plateau near <span class="nobr">0.19–0.20&nbsp;m/s</span>, a ramp down. A stall check must not fire on either&nbsp;ramp.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/linear-rail-sync/duty-speed-table.webp" alt="Table of 16 PWM settings with measured speed and duty, next to a chart of speed against duty with a fitted straight line" zoomable=true %}
    <figcaption class="prj-caption">Measured speed at 16 PWM settings (<span class="nobr">OCR&nbsp;10–160</span>, duty <span class="nobr">3.91–62.74%</span>) and the fitted line that turns position error into a speed&nbsp;command.</figcaption>
  </figure>
</div>

<div class="prj-media prj-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/linear-rail-sync/pwm-28-90khz.webp" alt="Oscilloscope screen: phase-correct PWM pulses, frequency readout 28.90 kHz, cursor duty 3.46 percent" zoomable=true %}
    <figcaption class="prj-caption">The existing <span class="nobr">phase-correct</span> PWM at OCR&nbsp;10: the counter reads 28.90&nbsp;kHz, over the 20&nbsp;kHz limit; the cursors read 3.46% duty against 3.91%&nbsp;nominal.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/linear-rail-sync/pwm-18-07khz.webp" alt="Oscilloscope screen: fast PWM pulses, frequency readout 18.07 kHz, cursor duty 13.4 percent" zoomable=true %}
    <figcaption class="prj-caption">The new fast PWM, counter reloaded to 155, at OCR&nbsp;165: the counter reads 18.07&nbsp;kHz, under the limit; the cursors read 13.4%&nbsp;duty.</figcaption>
  </figure>
</div>

## 4&nbsp;· Homing, fault recovery <span class="nobr">and the final run</span>

<p class="prj-caption">Feb.&nbsp;2021&nbsp;· step&nbsp;7&nbsp;· limit switches, GPIO fault&nbsp;lines</p>

- **Step 7: homing.** Before the first command, each rail runs backward at OCR0&nbsp;30 until its limit switch closes; the switch input idles high through a <span class="nobr">pull-up</span>. The MCU then zeroes its position and encoder counters and starts the controller.
- **Fault recovery.** A rail whose speed drops while it is still short of its target stops and raises its fault line, and a rail that sees the other's fault line stops too. After 1&nbsp;s both back off at OCR0&nbsp;40, and a switch on INT0 resets every variable for the next run.
- **Wiring.** Between the two ATmega128s I <span class="nobr">cross-wired</span> GPIO lines for "in position" and "stop", and each rail's limit switch sits on a <span class="nobr">pulled-up</span> input.
- **Not measured.** The reports log each rail's own position and error, not the offset between the two carriages, so this page claims no synchronization accuracy.

<div class="prj-media prj-media-2">
  <figure>
    <video src="{{ '/assets/video/projects/linear-rail-sync/final-sync-moves.mp4' | relative_url }}" poster="{{ '/assets/img/projects/linear-rail-sync/final-sync-moves-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">Final run, Feb.&nbsp;2021: both carriages leave the motor end together and make several moves side by&nbsp;side.</figcaption>
  </figure>
  <figure>
    <video src="{{ '/assets/video/projects/linear-rail-sync/final-fault-recovery.mp4' | relative_url }}" poster="{{ '/assets/img/projects/linear-rail-sync/final-fault-recovery-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">After one carriage was held by hand (cut from the clip), both rails stopped, ran back to the motor end and set off on a new move&nbsp;together.</figcaption>
  </figure>
</div>

## Debugging log

Faults I tracked down on this project, and how I found them.

<div class="prj-table-wrap prj-debug"><table><thead><tr><th>When</th><th>Symptom</th><th>How I found it</th><th>Fix</th></tr></thead><tbody>
<tr><td data-label="When">Sep.&nbsp;2020</td><td data-label="Symptom">A bench gearmotor ran slowly at 60% PWM, as if the signal did not reach&nbsp;it</td><td data-label="How I found it">Put the same PWM on the scope with and without a capacitor: without it the rising edges&nbsp;smeared</td><td data-label="Fix">Connected the capacitor; the motor then ran&nbsp;fast</td></tr>
<tr><td data-label="When">Nov.&nbsp;2020</td><td data-label="Symptom">Packed into 4 raw bytes, the distance lost its decimals; later the slave's encoder count changed while it was&nbsp;receiving</td><td data-label="How I found it">Serial logs: in a <span class="nobr">one-MCU</span> test 34.483 came back as 34.000; then the slave's count logged next to the received&nbsp;distance</td><td data-label="Fix">Scaled the distance by 10<sup>6</sup> before packing it; with one message type in the receive code the count stayed&nbsp;put</td></tr>
<tr><td data-label="When">Nov.&nbsp;2020</td><td data-label="Symptom">Under the UART lockstep the rails stuttered and&nbsp;crawled</td><td data-label="How I found it">Sketched speed against the segment targets: each wait for the other side's confirmation ramped the rail down to a&nbsp;stop</td><td data-label="Fix">Moved the handshake from UART to a dedicated GPIO&nbsp;line</td></tr>
<tr><td data-label="When">Jan.&nbsp;2021</td><td data-label="Symptom">Still stuttering on the GPIO line at Kp&nbsp;200; at Kp&nbsp;30 smooth but&nbsp;slower</td><td data-label="How I found it">Logged position, error and PWM command: the command dipped before every handover, and the window had to take in a 17.418&nbsp;mm&nbsp;error</td><td data-label="Fix">A window of 0.6&nbsp;×&nbsp;the segment (18&nbsp;mm for 30&nbsp;mm segments): the command stays at&nbsp;maximum</td></tr>
<tr><td data-label="When">Jan.&nbsp;2021</td><td data-label="Symptom">A stop check on unchanged position was rejected (marked ✗ in the&nbsp;report)</td><td data-label="How I found it">Segments did not advance every 10&nbsp;ms, so a stall check needed elapsed time: a&nbsp;speed</td><td data-label="Fix">Speed every 10&nbsp;ms in a timer interrupt; stop on a drop after cruise and raise the other rail's stop&nbsp;line</td></tr>
<tr><td data-label="When">Jan.&nbsp;2021</td><td data-label="Symptom">PWM at 28.90&nbsp;kHz, over the new driver's 20&nbsp;kHz limit; duty read 3.46% for 3.91%&nbsp;nominal</td><td data-label="How I found it">The driver's datasheet, then the scope's frequency counter and duty&nbsp;cursors</td><td data-label="Fix">Fast PWM with a counter reload in the overflow interrupt: 18.07&nbsp;kHz on the&nbsp;scope</td></tr>
</tbody></table></div>

## Session log

{% capture log_summary %}All {{ sessions.size }} progress reports, <span class="nobr">Aug.&nbsp;2020 – Feb.&nbsp;2021</span>{% endcapture %}
{% include prj_log.liquid sessions=sessions summary=log_summary %}

<div class="prj-ko" lang="ko">
<p><strong>한국어 요약</strong></p>
<p>2020년 8월부터 2021년 2월까지 IHLAB 학부연구생으로서 벨트 구동 리니어 레일 두 개가 함께 움직이도록 제어를 개발했습니다. 레일마다 엔코더가 달린 DC 기어모터와 ATmega128을 따로 두었고, 모터는 시판 <span class="nobr">H-브리지</span> 드라이버로 구동했습니다. 먼저 레일 하나의 PID 위치제어로 100&nbsp;mm 목표에 99.794&nbsp;mm까지 맞췄고, 이어서 위치 스트리밍(동기화 실패), 구간 궤적, UART 락스텝, GPIO 핸드셰이크와 인포지션 허용범위, 속도 저하 정지, 듀티 대비 속도 보정과 PWM 재설정, 리밋 스위치 원점 복귀와 고장 복구까지 일곱 단계를&nbsp;거쳤습니다.</p>
<p>버벅임은 게인을 낮추는 대신 원인을 찾아 해결했습니다. 로그를 보니 인포지션 허용범위가 17.418&nbsp;mm의 오차를 받아들이지 못해 레일이 구간마다 감속하고 있었고, 허용범위를 구간 길이의 0.6배(18&nbsp;mm)로 넓히자 레일이 끊김 없이 움직였습니다. 새 드라이버의 20&nbsp;kHz 제한에 맞춰 PWM을 28.90&nbsp;kHz에서 18.07&nbsp;kHz로 낮추고 오실로스코프로 확인했습니다. 보고서에는 레일별 위치와 오차만 있어서 두 레일 사이의 동기 정밀도는 수치로 제시하지&nbsp;않습니다.</p>
</div>

{% include prj_more.liquid %}
