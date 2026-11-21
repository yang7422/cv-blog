---
layout: page
title: ATmega128 from the Registers Up
description: "ATmega128 at register level: timer math checked on the scope, a keypad bug traced over four seminars, Aug. –⁠ Dec. 2019"
img: assets/img/projects/atmega128/thumb.webp
importance: 4
---

<!-- Session data: _data/ihlab_seminars.yml, project 'atmega' (the 2019 microprocessor decks plus the two Dec. 2019 decks of the DYNAMIXEL archive). Styles: "Project pages" in _sass/_custom.scss. -->
{%- assign sessions = site.data.ihlab_seminars | where: 'project', 'atmega' -%}

From August to December 2019, as an undergraduate researcher at IHLAB (Tech University of Korea), I learned the ATmega128 microcontroller from the registers up, one peripheral at a time, and presented each step at the lab seminar.
On the lab’s training kit I programmed GPIO, external interrupts, Timer2 in all four of its modes, a character LCD with custom characters, and USART serial, working the numbers out first and then checking them on the oscilloscope or a PC terminal.
The series ended with the choice of a DYNAMIXEL robot arm as the winter project, the start of my <span class="nobr">legged-robot</span> work.

<div class="prj-stats">
  <div class="prj-stat"><span class="prj-stat-value">{{ sessions.size }}</span><span class="prj-stat-label">lab seminars, <span class="nobr">Aug. – Dec.&nbsp;2019</span></span></div>
  <div class="prj-stat"><span class="prj-stat-value">37</span><span class="prj-stat-label">FEEDBACK slides following up the previous talk’s&nbsp;questions</span></div>
  <div class="prj-stat"><span class="prj-stat-value">3</span><span class="prj-stat-label">timer modes derived by hand, then checked on the&nbsp;scope</span></div>
  <div class="prj-stat"><span class="prj-stat-value">4</span><span class="prj-stat-label">seminars on one keypad bug, each with a test&nbsp;video</span></div>
</div>

## What this project shows

<div class="prj-traits">
  <div class="prj-trait">
    <strong>Derive first, then measure</strong>
    <p>For the <span class="nobr">1-second</span> exercise in three Timer2 modes, I worked the constants out on paper from the kit’s 14.7456&nbsp;MHz crystal: tick length, overflow count, compare value, duty cycle. Then I checked each period with the oscilloscope’s cursors in normal, CTC and fast PWM&nbsp;modes.</p>
  </div>
  <div class="prj-trait">
    <strong>Stay with a bug until it is understood</strong>
    <p>The keypad took four seminars: first it read only 0, then one press filled all four digits. I filmed it at each of those seminars, fixed one cause at a time, and said plainly what still did not&nbsp;work.</p>
  </div>
  <div class="prj-trait">
    <strong>Down to the bit</strong>
    <p>I drew my name as six custom LCD characters and worked out their 48 bytes by hand. When the screen stayed blank, the cause was in the program: it never wrote a character code to display memory, so nothing told the display to show&nbsp;them.</p>
  </div>
  <div class="prj-trait">
    <strong>Questions answered in writing</strong>
    <p>Six talks open with FEEDBACK slides that follow up the previous talk’s questions, 37 slides in all. I also corrected a textbook figure, and my own description of a register bit a week after presenting&nbsp;it.</p>
  </div>
</div>

## Timeline

{% include prj_timeline.liquid sessions=sessions start='2019-08-19' weeks=19 ticks='2019-09-02|Sep 2019,2019-10-07|Oct 2019,2019-11-04|Nov 2019,2019-12-02|Dec 2019' noun='seminars' %}
<p class="prj-caption">One mark per seminar, one column per week. Hover, tap or tab to a mark for its topic; the full list is in the log at the end.</p>

## Derive on paper, then check on the scope

- **One clock behind every constant.** The kit runs on a 14.7456&nbsp;MHz crystal. With the /8 prescaler, one timer tick is 0.5425&nbsp;µs and one <span class="nobr">256-count</span> overflow 138.89&nbsp;µs, so 7200 overflows make a second. I worked out each mode’s constants this way and used them in its code.
- **Three modes, one target.** For a <span class="nobr">1-second</span> period, normal mode toggles a pin every 3600 overflows. CTC mode uses /1024 (69.44&nbsp;µs per tick), OCR2&nbsp;=&nbsp;72 and 100 compare matches. In fast PWM mode, the 7200 periods of each second are counted in software and split at 6000, an 83% duty cycle. In all three, the scope cursors read Δ1.00&nbsp;s.
- **A correction for the record.** The CTC constant is off by one. In CTC mode the counter runs from 0 to OCR2, so OCR2&nbsp;=&nbsp;72 means 73 ticks per match, and the code as written gives a period of 1.014&nbsp;s, not 1.000&nbsp;s. The <span class="nobr">hand-placed</span> cursors did not catch the 14&nbsp;ms difference; OCR2&nbsp;=&nbsp;71 gives exactly 1.000&nbsp;s.
- **A datasheet question, tested.** To follow up a seminar question about when a new OCR2 value takes effect in <span class="nobr">phase-correct</span> PWM, I wrote two versions, one rewriting OCR2 in the overflow interrupt and one in both the overflow and compare interrupts, and marked up the datasheet’s timing diagram for each. The scope’s frequency readout showed 3.61407&nbsp;kHz for both, against the 3614.12&nbsp;Hz expected from <span class="nobr">14.7456&nbsp;MHz ÷ (8 × 510)</span>.

<div class="prj-media prj-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/atmega128/timer-normal.webp" alt="Handwritten derivation of the Timer2 normal-mode constants beside an oscilloscope photo of a square wave whose cursors are 1.00 s apart" zoomable=true %}
    <figcaption class="prj-caption">Normal mode, 7&nbsp;Nov&nbsp;2019: 0.5425&nbsp;µs per tick, 7200 overflows per second, a toggle every 3600, and Δ1.00&nbsp;s on the scope. Notes and slides are in Korean; click to&nbsp;zoom.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/atmega128/timer-ctc.webp" alt="Handwritten derivation for Timer2 in CTC mode, OCR2 = 72 and 100 matches, beside the oscilloscope capture" zoomable=true %}
    <figcaption class="prj-caption">CTC mode: 69.44&nbsp;µs per tick at /1024, OCR2&nbsp;=&nbsp;72 and 100 matches. The cursors read Δ1.00&nbsp;s; with 73 ticks per match, the code as written gives 1.014&nbsp;s.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/atmega128/timer-fast-pwm.webp" alt="Handwritten duty-cycle derivation for fast PWM, 6000 of 7200 or about 83 percent, beside the oscilloscope capture" zoomable=true %}
    <figcaption class="prj-caption">Fast PWM: 7200 periods per second, split at 6000 for a duty cycle of <span class="nobr">5/6 ≈ 83%</span>. The cursors read Δ1.00&nbsp;s.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/atmega128/pc-pwm-ocr2.webp" alt="Code that rewrites OCR2 in the Timer2 overflow interrupt, beside a scope photo whose frequency readout shows 3.61407 kHz" zoomable=true %}
    <figcaption class="prj-caption"><span class="nobr">Phase-correct</span> PWM with OCR2 rewritten in the overflow interrupt, 22&nbsp;Nov&nbsp;2019. The readout shows 3.61407&nbsp;kHz; <span class="nobr">14.7456&nbsp;MHz ÷ (8 × 510)</span> gives 3614.12&nbsp;Hz.</figcaption>
  </figure>
</div>

## One keypad bug, four seminars

- **One cause at a time.** In October the 4×4 keypad showed only 0. By 7&nbsp;Nov keys registered, but one press filled all four digits. For 14&nbsp;Nov I fixed two errors in the scan, rows driven high where they should have been driven low and a <span class="nobr">key-index</span> formula that gave the wrong numbers, but the flood remained: the loop read a held key again on every pass.
- **From a delay to edge detection.** A 0.25&nbsp;s <span class="nobr">hold-off</span> after each digit then gave one digit per press, as long as the key was released within 0.25&nbsp;s (14&nbsp;Nov). In the same talk I said that versions driven by interrupts or the timer did not work yet. A week later I replaced the delay with edge detection: a key counts only when the scan result changes.
- **What a button really does.** In October, INT0 on a falling edge toggled all eight LEDs. In a December drill, where each INT0 press stepped through four LED patterns, I boxed two spikes on the scope just before a clean edge: switch bounce, each spike an extra edge that the interrupt could count as a press.

<div class="prj-media prj-media-2">
  <figure>
    <video src="{{ '/assets/video/projects/atmega128/keypad-before.mp4' | relative_url }}" poster="{{ '/assets/img/projects/atmega128/keypad-before-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">7&nbsp;Nov&nbsp;2019: one press fills all four digits (2222, 3333,&nbsp;1111).</figcaption>
  </figure>
  <figure>
    <video src="{{ '/assets/video/projects/atmega128/keypad-after.mp4' | relative_url }}" poster="{{ '/assets/img/projects/atmega128/keypad-after-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">14&nbsp;Nov: one digit per press, shifting left: 2512&nbsp;→&nbsp;5123&nbsp;→&nbsp;1234&nbsp;→&nbsp;2345.</figcaption>
  </figure>
  <figure>
    <video src="{{ '/assets/video/projects/atmega128/int0-leds.mp4' | relative_url }}" poster="{{ '/assets/img/projects/atmega128/int0-leds-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">Oct.&nbsp;2019: INT0 on a falling edge toggles all eight LEDs at each&nbsp;press.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/atmega128/switch-bounce.webp" alt="Oscilloscope photo dated 24 Dec 2019: a switch edge with two short spikes before the signal settles" zoomable=true %}
    <figcaption class="prj-caption">24&nbsp;Dec&nbsp;2019, interrupt drill: a switch edge at 20&nbsp;ms per division, with two spikes before the level&nbsp;settles.</figcaption>
  </figure>
</div>

## My name in 48 bytes

- **Pixel by pixel.** The LCD controller has a small RAM, CGRAM, for characters the user draws. I drew the three syllables of my name (양건모) on <span class="nobr">5 × 8</span> grids, two characters per syllable, worked out the 48 bytes by hand, and wrote them to CGRAM with the <span class="nobr">set-address</span> commands 0x40 to 0x68.
- **A blank screen, explained.** On 14&nbsp;Nov the LCD stayed blank. The code wrote the glyphs into CGRAM but never wrote a character code into DDRAM, the memory that holds what the screen shows, and it set the cursor before initializing the LCD. On 21&nbsp;Nov, with initialization first and six DDRAM writes (codes <span class="nobr">0x00–0x05</span>), my name appeared.

<div class="prj-media">
  <figure>
    {% include figure.liquid path="assets/img/projects/atmega128/lcd-glyphs.webp" alt="Three 10-by-8 pixel grids that draw the Hangul syllables of the author's name, with the six 8-byte arrays below them" zoomable=true %}
    <figcaption class="prj-caption">The three syllables of my name on <span class="nobr">5 × 8</span> grids, two characters each, and the 48 bytes I typed from them (14&nbsp;Nov&nbsp;2019).</figcaption>
  </figure>
</div>
<div class="prj-media prj-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/atmega128/lcd-blank-nov14.webp" alt="The training kit with its 16-by-2 character LCD lit but blank" zoomable=true %}
    <figcaption class="prj-caption">14&nbsp;Nov: glyphs in CGRAM, nothing in DDRAM, and the screen stays&nbsp;blank.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/atmega128/lcd-name-nov21.webp" alt="The character LCD showing the author's name in six custom glyphs" zoomable=true %}
    <figcaption class="prj-caption">21&nbsp;Nov: after six DDRAM writes, the LCD shows 양건모. It matches the bytes cell for cell, including one slip: two rows of the first glyph were typed as 0x0d where the drawing has&nbsp;0x0e.</figcaption>
  </figure>
</div>

## Reading the board and the books

- **The kit’s schematic, block by block.** On 19&nbsp;Sep I went through the schematic of the lab’s ATmega128 training kit one block at a time: oscillator, reset, analog supply filter, switches, LEDs, and the <span class="nobr">RS-232</span> and USB interfaces. The schematic is the kit’s own sheet (“ATMEGA128KIT”, dated 2010), not my design. My part was a note on what each component does, such as the diode that drains the leftover voltage at <span class="nobr">power-off</span>.
- **One crystal, followed into the firmware.** My note on the oscillator says the kit uses a 14.7456&nbsp;MHz crystal to match the serial clock. On 21&nbsp;Nov I boxed its column in the <span class="nobr">baud-rate</span> table (0.0% error), set UBRR to <span class="nobr">14745600 ÷ (16 × 115200)</span> <span class="nobr">− 1 = 7</span>, and a PC terminal received “Serial Comm Test”.
- **Sources checked, my own included.** A textbook figure labelled +10&nbsp;V on an <span class="nobr">RS-232</span> line as mark “0”. I corrected it to space, with mark “1” at the negative level, as in the level table on the same slide. My 21&nbsp;Nov script said the UCPOL bit is used only in transmit mode; after a question, the 28&nbsp;Nov talk corrected it: UCPOL is for synchronous mode, where it sets when output data changes and when input data is sampled.

<div class="prj-media prj-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/atmega128/kit-oscillator-reset.webp" alt="Slide crop with notes on the crystal oscillator and reset circuits, the datasheet's crystal connection figure and capacitor table with 12 to 22 pF boxed, a reset truth table and a reference reset circuit" zoomable=true %}
    <figcaption class="prj-caption">From my study of the kit’s schematic, 19&nbsp;Sep&nbsp;2019: notes on the oscillator and reset circuits, beside the datasheet’s crystal figure with its <span class="nobr">12–22&nbsp;pF</span> capacitor range boxed, and a reference reset&nbsp;circuit.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/atmega128/rs232-correction.webp" alt="RS-232 level table above a textbook timing figure in which the label at plus 10 volts is corrected from mark to space" zoomable=true %}
    <figcaption class="prj-caption">21&nbsp;Nov: my <span class="nobr">RS-232</span> level table above a textbook figure I corrected. At +10&nbsp;V the line is a space (logic 0), not a&nbsp;mark.</figcaption>
  </figure>
</div>

## Debugging log

Faults from these five months, and how each one was found.

<div class="prj-table-wrap prj-debug"><table><thead><tr><th>When</th><th>Symptom</th><th>How I found it</th><th>Fix</th></tr></thead><tbody>
<tr><td data-label="When"><span class="nobr">Oct. – Nov.&nbsp;2019</span></td><td data-label="Symptom">The keypad read only 0 (Oct.); by 7&nbsp;Nov keys registered, but one press filled all four&nbsp;digits</td><td data-label="How I found it">Filmed it at each seminar and went back over the scan code: rows driven high instead of low, a <span class="nobr">key-index</span> formula that gave the wrong numbers, and a loop that read a held key on every&nbsp;pass</td><td data-label="Fix">Fixed the drive level and the index, then added a 0.25&nbsp;s <span class="nobr">hold-off</span> after each digit (14&nbsp;Nov)</td></tr>
<tr><td data-label="When">Nov.&nbsp;2019</td><td data-label="Symptom">With the <span class="nobr">hold-off</span>, a key held longer than 0.25&nbsp;s still&nbsp;repeated</td><td data-label="How I found it">I said so in the 14&nbsp;Nov talk, and the seminar asked me to redo the keypad with a&nbsp;trigger</td><td data-label="Fix">Edge detection: a key counts only when the scan result changes (21&nbsp;Nov)</td></tr>
<tr><td data-label="When">Nov.&nbsp;2019</td><td data-label="Symptom">My custom characters did not appear; the LCD stayed&nbsp;blank</td><td data-label="How I found it">The code on my 14&nbsp;Nov slide wrote the glyphs into CGRAM but no character code into DDRAM, and set the cursor before&nbsp;initialization</td><td data-label="Fix">Initialized first, then wrote codes <span class="nobr">0x00–0x05</span> to DDRAM; my name appeared (21&nbsp;Nov)</td></tr>
<tr><td data-label="When">Nov.&nbsp;2019</td><td data-label="Symptom">A textbook figure labelled +10&nbsp;V on an <span class="nobr">RS-232</span> line as mark&nbsp;“0”</td><td data-label="How I found it">Checked it against the level table: mark (logic 1) is <span class="nobr">−3 to −25&nbsp;V</span>, space (logic 0) is <span class="nobr">+3 to +25&nbsp;V</span></td><td data-label="Fix">Corrected the figure on my slide: space at +10&nbsp;V, mark “1” at the low&nbsp;level</td></tr>
<tr><td data-label="When">Nov.&nbsp;2019</td><td data-label="Symptom">My 21&nbsp;Nov script said the UCPOL bit is used only in transmit&nbsp;mode</td><td data-label="How I found it">A question at the seminar, answered on a Q&amp;A slide the next&nbsp;week</td><td data-label="Fix">Corrected on 28&nbsp;Nov: UCPOL is for synchronous mode, where it sets when output data changes and when input data is&nbsp;sampled</td></tr>
</tbody></table></div>

## Seminar log

{% capture log_summary %}All {{ sessions.size }} seminars, <span class="nobr">Aug. – Dec.&nbsp;2019</span>{% endcapture %}
{% include prj_log.liquid sessions=sessions summary=log_summary %}

<div class="prj-ko" lang="ko">
<p><strong>한국어 요약</strong></p>
<p>2019년 8월부터 12월까지 한국공학대학교 IHLAB 학부연구생으로 ATmega128을 레지스터 수준에서 주변장치 하나씩 익히고, 단계마다 랩 세미나에서 발표했습니다. 타이머 상수는 14.7456&nbsp;MHz 클럭에서 손으로 계산한 뒤 오실로스코프로 확인했고(일반·CTC·고속 PWM 모드 모두 커서 간격 1.00초), 위상 정정 PWM 출력은 3.61407&nbsp;kHz로, 클럭에서 예상되는 3614.12&nbsp;Hz와 일치했습니다. 다만 CTC 설정은 한 카운트가 어긋나 있어서, 슬라이드의 코드대로라면 주기가 1.014초라는 점도 함께&nbsp;적었습니다.</p>
<p>키패드 버그는 네 번의 세미나에 걸쳐 다뤘습니다. 구동 레벨과 키 인덱스를 바로잡았고, 누르고 있는 키가 반복 입력되는 문제는 처음엔 0.25초 지연으로, 다음 주에는 엣지 검출로 해결했습니다. 제 이름은 5×8 글리프 6개(48바이트)로 직접 그려 LCD에 띄웠습니다. 지난 발표에서 받은 질문에는 FEEDBACK 슬라이드 37장으로 답했고, 교재의 <span class="nobr">RS-232</span> 그림 오류도 바로잡았습니다. 학기 말에는 다이나믹셀 로봇팔을 겨울방학 프로젝트로&nbsp;정했습니다.</p>
</div>

{% include prj_more.liquid %}
