---
layout: page
title: Person‑Following Robot and Its Boards
description: "Radio‑synced ultrasonic ranging and five boards I designed and built: two in 2020, three for the graduation project (Mar. 2020 –⁠ Oct. 2021)"
img: assets/img/projects/person-following-robot/thumb.webp
importance: 1
---

<!-- Session data: _data/ihlab_seminars.yml, project 'follow' (from sessions.yml of this page). Styles: "Project pages" in _sass/_custom.scss. -->

{%- assign sessions = site.data.ihlab_seminars | where: 'project', 'follow' -%}

As an undergraduate researcher at IHLAB (Tech University of Korea), I developed the sensing side of a robot that follows a person, from Mar.&nbsp;2020 to Oct.&nbsp;2021. The person carries a small transmitter, and a radio message tells the robot when its 40&nbsp;kHz ultrasonic burst leaves, so every receiver on the robot times a <span class="nobr">one-way</span> flight. Because every range rests on that timing, I accounted for the radio's latency and kept the transmitter and receivers in sync, which let the robot locate the person precisely and follow them accurately. In 2020 this following unit was my own project, including two boards I designed, assembled by hand once the bare PCBs arrived, and brought up. In 2021 it became my part of a <span class="nobr">three-person</span> graduation project, a <span class="nobr">material-transport</span> robot for construction sites, and I designed and built three more boards for&nbsp;it.

<div class="prj-stats">
  <div class="prj-stat"><span class="prj-stat-value">{{ sessions.size }}</span><span class="prj-stat-label">lab seminars, <span class="nobr">Mar.&nbsp;2020 – Jul.&nbsp;2021</span></span></div>
  <div class="prj-stat"><span class="prj-stat-value">5</span><span class="prj-stat-label">boards I designed and built: 2&nbsp;<span class="nobr">hand-assembled</span> and brought&nbsp;up, 3&nbsp;for the graduation&nbsp;project</span></div>
  <div class="prj-stat"><span class="prj-stat-value">84<span class="prj-unit">µs</span></span><span class="prj-stat-label">trigger skew between transmitter and receiver after tuning, down from 428&nbsp;µs</span></div>
  <div class="prj-stat"><span class="prj-stat-value">519</span><span class="prj-stat-label">radio exchanges logged to check the <span class="nobr">lost-packet</span>&nbsp;handling</span></div>
</div>

## What this project shows

<div class="prj-traits">
  <div class="prj-trait">
    <strong>Circuits I design, assemble and bring up</strong>
    <p>Two <span class="nobr">2-layer</span> STM32F405 boards drawn in OrCAD in Jul.&nbsp;2020 and soldered by hand, with traces sized by <span class="nobr">IPC-2221</span> and vias enlarged for current. At <span class="nobr">bring-up</span> I found a missing ISP supply and an LDO dropout, and scoped the regulator input in four capacitor&nbsp;combinations.</p>
  </div>
  <div class="prj-trait">
    <strong>Measured against ground truth</strong>
    <p>Targets stood at set distances and angles, on paper laid out on the floor or a <span class="nobr">hand-drawn</span> 10&nbsp;cm grid board, and timing came from <span class="nobr">two-channel</span> scope captures. After I <span class="nobr">re-mounted</span> the receivers, every point from 0 to 40° at 100 and 150&nbsp;cm read within 3.6&nbsp;cm and&nbsp;2°.</p>
  </div>
  <div class="prj-trait">
    <strong>Causes before filters</strong>
    <p>Range spikes turned out to be reflections; once a lower drive voltage removed them, the median filter came out again. Latency jitter traced to a polling loop slowed by a debug print, a silent radio was a CE pin never raised, and 2.29&nbsp;ms of command overhead explained ≈78 of an 82&nbsp;cm&nbsp;offset.</p>
  </div>
  <div class="prj-trait">
    <strong>Dead ends on record</strong>
    <p>Even with echo amplitudes matched, a 90° <span class="nobr">wide-angle</span> receiver returned data only at <span class="nobr">25–45&nbsp;cm</span> with our transmitter. I measured why (≈57 vs. ≈3.8&nbsp;Vpp drive, different attenuation) and kept the old receivers. Vertical localization failed beyond about&nbsp;10°.</p>
  </div>
</div>

## Timeline

{% include prj_timeline.liquid sessions=sessions start='2020-03-23' weeks=69 ticks='2020-04-06|Apr 2020,2020-07-06|Jul 2020,2020-10-05|Oct 2020,2021-01-04|Jan 2021,2021-04-05|Apr 2021,2021-07-05|Jul 2021' parts='2020|Following unit and my own boards,2021|Graduation project' noun='seminars' %}

<p class="prj-caption">One mark per seminar, one column per week. Hover, tap or tab to a mark for its topic; the full list is in the log at the end.</p>

## Boards I designed

- **Two boards, designed, <span class="nobr">hand-assembled</span> and brought up.** In Jul.&nbsp;2020 I analyzed the lab's earlier RF board and a revision of its power and radio sections, then drew the <span class="nobr">robot-side</span> receiver board in OrCAD Capture and OrCAD Layout, through at least four layout versions; a handheld transmitter board followed. Both are <span class="nobr">2-layer</span> boards around an STM32F405RG with an nRF24L01+ radio header; once the bare PCBs were fabricated, I soldered the parts on by hand. The <span class="nobr">robot-side</span> board takes 24&nbsp;V through a polyfuse and a series Schottky diode into an <span class="nobr">LM2576S-5</span> buck and an <span class="nobr">LM1117-3.3</span>, and adds <span class="nobr">RS-485</span>, a buzzer driver and four ultrasonic ports. I also compiled a <span class="nobr">26-slide</span> OrCAD guide: its layout rules are shown on my own boards, and 7 of its slides come from an external&nbsp;tutorial.
- **Sized for current, checked before fabrication.** I sized the traces with an <span class="nobr">IPC-2221</span> calculator: 30.8&nbsp;mil for 1&nbsp;A at a 10&nbsp;°C rise, its <span class="nobr">internal-layer</span> result, which errs wide on a <span class="nobr">2-layer</span> board. I enlarged the vias from 0.762/0.381 to 1.000/0.700&nbsp;mm pad/drill, which leaves exactly the fab house's 0.15&nbsp;mm minimum annular ring. After the lab's review I renumbered a <span class="nobr">10-pin</span> header footprint that had been numbered like a DIP&nbsp;part.
- **<span class="nobr">Bring-up</span>, measured.** The handheld board's <span class="nobr">ST-LINK</span> would not attach because I had left target VCC off the ISP header; a bodge wire to MCU_VDD fixed it. Its 3.3&nbsp;V rail read 2.8&nbsp;V because the LM1117 needs at least 4.75&nbsp;V and the battery gives 3.8&nbsp;V, so I switched to an AME8801AEEV <span class="nobr">low-dropout</span> regulator. On the <span class="nobr">robot-side</span> board I fitted the buck converter's input capacitors in four combinations and scoped the rail each time: only both together gave a clean&nbsp;rail.
- **<span class="nobr">Add-ons</span>, then three more boards.** In Nov.&nbsp;2020 I designed two perfboard <span class="nobr">add-ons</span> for a <span class="nobr">wide-beam</span> transducer: a <span class="nobr">single-transistor</span> level shifter for its <span class="nobr">4–5&nbsp;V</span> trigger input, and an <span class="nobr">LM2940CS-12</span> regulator soldered onto the <span class="nobr">robot-side</span> board, because at 5&nbsp;V the transducer fell far short of 3&nbsp;m. For the graduation project I designed three more boards, laid them out by Jul.&nbsp;2021 and then built&nbsp;them.

<div class="prj-media">
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/buck-stage-schematic-layout-board.webp" alt="One buck converter shown three ways: the schematic with PU1 LM2576S-5, PL1 and PD2 on top, and below it the OrCAD layout of that area next to a photo of the same area on the assembled board" zoomable=true %}
    <figcaption class="prj-caption">One buck converter on the <span class="nobr">robot-side</span> board, three ways, all one revision: my schematic and OrCAD layout (Jul.&nbsp;2020) and the board I assembled (photo from a Nov.&nbsp;2020 seminar). The designators match (PU1&nbsp;<span class="nobr">LM2576S-5</span>, PL1, CE1); the fitted CE1 reads 47&nbsp;µF where the schematic says 100&nbsp;µF.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/main-board-layout-vs-assembled.webp" alt="The final OrCAD layout of the robot-side receiver board next to a photo of the assembled board, aligned so that the same parts sit in the same places" zoomable=true %}
    <figcaption class="prj-caption">The <span class="nobr">robot-side</span> receiver board: final layout (Jul.&nbsp;2020) and the board I assembled (photo from a Nov.&nbsp;2020 seminar), aligned on the four mounting holes. STM32F405RG, radio header, ISP and buzzer; down the right edge, four ultrasonic ports and the <span class="nobr">RS-485</span> port by the MAX485, three of the five&nbsp;fitted.</figcaption>
  </figure>
  <figure>
    <div class="prj-row">
      <div style="flex: 1.302 1 0%">{% include figure.liquid path="assets/img/projects/person-following-robot/receiver-board-layout-1.webp" alt="OrCAD Layout of the robot-side receiver board, first pass: parts placed, with unrouted connections still drawn as thin lines" zoomable=true %}</div>
      <div style="flex: 1.080 1 0%">{% include figure.liquid path="assets/img/projects/person-following-robot/receiver-board-layout-2.webp" alt="Second layout pass of the same board" zoomable=true %}</div>
    </div>
    <div class="prj-row">
      <div style="flex: 1.062 1 0%">{% include figure.liquid path="assets/img/projects/person-following-robot/receiver-board-layout-3.webp" alt="An intermediate version of the same board layout, from the OrCAD guide" zoomable=true %}</div>
      <div style="flex: 1.061 1 0%">{% include figure.liquid path="assets/img/projects/person-following-robot/receiver-board-layout-final.webp" alt="The final layout of the robot-side receiver board, the version that was fabricated" zoomable=true %}</div>
    </div>
    <figcaption class="prj-caption">The <span class="nobr">robot-side</span> board, pass by pass in OrCAD Layout (Jul.&nbsp;2020): my first and second passes of 15&nbsp;Jul. (top; the first still has unrouted connections), then an intermediate version from my OrCAD guide and the final layout of 29&nbsp;Jul. (bottom), the one that was&nbsp;fabricated.</figcaption>
  </figure>
</div>

<div class="prj-media prj-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/via-and-footprint-fixes.webp" alt="Close-ups from the OrCAD layout: a small via and the enlarged via, then a 10-pin header footprint before and after its pads were renumbered" zoomable=true %}
    <figcaption class="prj-caption">Two fixes before fabrication (Jul.&nbsp;2020). Left: a via before and after I enlarged it for current, from 0.762/0.381 to 1.000/0.700&nbsp;mm pad/drill. Right: a <span class="nobr">10-pin</span> header footprint numbered like a DIP part, and the same header renumbered&nbsp;odd/even.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/handheld-board-layout-and-bodge.webp" alt="The final layout of the handheld transmitter board next to a photo of its underside with a wire soldered from the 6-pin ISP header to a decoupling capacitor" zoomable=true %}
    <figcaption class="prj-caption">The handheld transmitter board: final layout, and its underside at <span class="nobr">bring-up</span> (Aug.&nbsp;2020). The bodge wire at the top brings MCU_VDD to the ISP header, so the <span class="nobr">ST-LINK</span> could&nbsp;attach.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/decoupling-test.webp" alt="Four oscilloscope captures of the same supply rail at power-up: clean, with periodic dips, with slight noise, and with heavy spikes" zoomable=true %}
    <figcaption class="prj-caption">My board's buck input at <span class="nobr">power-up</span>, capacitor by capacitor (8&nbsp;Aug.&nbsp;2020); the rail rises to ≈23&nbsp;V. Both fitted (top left): clean. Ceramic only (top right): dips at a regular interval. Electrolytic only (bottom left): slight noise. Neither (bottom right): heavy&nbsp;spikes.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/perfboard-add-ons.webp" alt="A small hand-wired perfboard carrying an LM2940CS-12 regulator soldered onto the green board, and an oscilloscope showing a 3.3 V pulse and the inverted 5 V pulse it produces" zoomable=true %}
    <figcaption class="prj-caption">Two perfboard <span class="nobr">add-ons</span> (Nov.&nbsp;2020). Left: the <span class="nobr">LM2940CS-12</span> regulator soldered onto the <span class="nobr">robot-side</span> board. Right: the level shifter on the scope, turning the MCU's 3.3&nbsp;V pulse (blue) into an inverted 5&nbsp;V pulse&nbsp;(yellow).</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/pcb-manual-page.webp" alt="Slide from the OrCAD guide: the LM1117 regulator schematic, and a wrong and a right way to route its input past the capacitors on the robot-side board" zoomable=true %}
    <figcaption class="prj-caption">A page of the <span class="nobr">26-slide</span> OrCAD guide I compiled, shown on my own board: route the regulator's input through its capacitors first (wrong, top; right, bottom). Slides are in Korean; click to&nbsp;zoom.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/layouts-2021.webp" alt="Three PCB layouts: a dense controller board with dimension lines, a handheld target board, and a wide remote-control board with dimension lines" zoomable=true %}
    <figcaption class="prj-caption">The three boards I designed for the graduation project, as laid out in Jul.&nbsp;2021 (not to scale): the STM32F429 following controller (<span class="nobr">80.797 × 74.435&nbsp;mm</span>), the handheld target and the manual remote (<span class="nobr">134.880 × 77.630&nbsp;mm</span>). I built all three&nbsp;afterwards.</figcaption>
  </figure>
</div>

## Ranging and the radio link (2020)

- **<span class="nobr">One-way</span> ranging.** A radio message announces each ultrasonic burst, so every receiver on the robot times a <span class="nobr">one-way</span> flight, and two or three ranges give distance and bearing. I worked out how range error becomes angle error: with receivers 45&nbsp;cm apart, ±1&nbsp;cm of range error shifts the computed angles by 2.34° at 50&nbsp;cm and 2.53° at 150&nbsp;cm.
- **Sensors measured before they were chosen.** I tested the candidates at set distances and angles. The <span class="nobr">HC-SR04</span> stayed within <span class="nobr">−1.08 to +0.99&nbsp;%</span> at <span class="nobr">5–50&nbsp;cm</span>. Three SRF02 sensors triangulated within 1&nbsp;cm and 1.6°, but I set them aside for the rest of 2020: over I²C a reading needed more than 65&nbsp;ms (70&nbsp;ms by the datasheet), and the incidence angle was only 30°. Before that, a constant 82&nbsp;cm offset in <span class="nobr">one-way</span> SRF02 ranging turned out to be mostly command overhead: the 2.29&nbsp;ms between the listen and burst commands explains ≈78&nbsp;cm of&nbsp;it.
- **Causes, not filters.** Two transmitters gave unstable ranges, including a 35&nbsp;µs <span class="nobr">echo-arrival</span> jitter (1.19&nbsp;cm), so I moved to one transmitter and several receivers. Range spikes from the <span class="nobr">HG-M40DB</span> transducer during fast motion then survived both an RC <span class="nobr">low-pass</span> filter I derived and a median filter. I traced them to reflections, swept the drive voltage against the acceptance angle and settled on 9&nbsp;V (12&nbsp;V spiked even with the robot standing still), then dropped the median filter, which only slowed the&nbsp;response.
- **The radio link, end to end.** I wrote a <span class="nobr">register-level</span> nRF24L01+ driver on two ATmega128s, pinned its latency at a constant 6.01&nbsp;ms and ported it to STM32 with HAL. Tuning both sides together in Nov.&nbsp;2020 cut the trigger skew from 428 to 84&nbsp;µs and the sampling period from 49.9 to 34.0&nbsp;ms, with ranges read out to 388&nbsp;cm. Bearing stayed the weak point: a target at 40° read 53°, and the <span class="nobr">wide-beam</span> transducer I tried next returned no echo <span class="nobr">15° or more</span>&nbsp;<span class="nobr">off-axis</span>.

<div class="prj-media prj-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/reception-map.webp" alt="Top view of white sheets on the floor with blue dots marking transmitter positions and orange curves marking the reception boundary; the receiver bar is boxed at the bottom" zoomable=true %}
    <figcaption class="prj-caption">Where the receivers still hear the transmitter (May&nbsp;2020). Each dot is a transmitter position on the paper laid out on the floor, the orange curves trace the widest angle that still returned a range, and the receiver bar sits in the box at the&nbsp;bottom.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/end-to-end-tuning.webp" alt="Four oscilloscope captures: two triggers 428 microseconds apart and then 84 microseconds apart, and a sampling period of 49.9 ms and then 34.0 ms" zoomable=true %}
    <figcaption class="prj-caption">Tuning transmitter and receiver together (<span class="nobr">7–8&nbsp;Nov.&nbsp;2020</span>). Top: the skew between their ultrasonic triggers, Δ428&nbsp;µs before and Δ84.0&nbsp;µs after. Bottom: the sampling period, Δ49.9&nbsp;ms (20.03&nbsp;Hz) before and Δ34.0&nbsp;ms (29.41&nbsp;Hz)&nbsp;after.</figcaption>
  </figure>
</div>

### In the lab

Phone clips, photos and scope captures from my weekly seminar slides, in date&nbsp;order.

<div class="prj-media prj-media-2">
  <figure>
    <video src="{{ '/assets/video/projects/person-following-robot/hc-sr04-echo-vs-distance-2020-03.mp4' | relative_url }}" poster="{{ '/assets/img/projects/person-following-robot/hc-sr04-echo-vs-distance-2020-03-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">The project's first seminar (Mar.&nbsp;2020): on the scope, the echo pulse of an <span class="nobr">HC-SR04</span> (yellow) widens and narrows as the distance&nbsp;changes.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/hc-sr04-first-echo.webp" alt="An HC-SR04 ultrasonic sensor held against a ruler 10 cm above a desk, next to an oscilloscope capture of its echo pulse with cursors 595 microseconds apart" zoomable=true %}
    <figcaption class="prj-caption">From the same seminar: the sensor held 10&nbsp;cm above the desk against a ruler. My program read 3.355&nbsp;cm, but the echo on the scope was about 600&nbsp;µs wide, which is 10.2&nbsp;cm at 340&nbsp;m/s, so I went after my timer&nbsp;code.</figcaption>
  </figure>
  <figure>
    <div class="prj-row">
      <div style="flex: 1.333 1 0%">{% include figure.liquid path="assets/img/projects/person-following-robot/ts601-sheets.webp" alt="Grid sheets with pencil marks laid over a table, an aluminum bar with two receivers at the far end and transmitters at the near edge" zoomable=true %}</div>
      <div style="flex: 1.667 1 0%">{% include figure.liquid path="assets/img/projects/person-following-robot/ts601-jitter-scope.webp" alt="Oscilloscope capture with cursors 35 microseconds apart on a falling edge" zoomable=true %}</div>
    </div>
    <figcaption class="prj-caption">TS601 tests on grid sheets marked by hand, with the receiver bar at the far end (May&nbsp;2020). Right: with two transmitters, the echo edge wandered by 35&nbsp;µs (1.19&nbsp;cm), so I moved to one transmitter and several&nbsp;receivers.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/spike-hunt-bench.webp" alt="A lab table covered with grid sheets; at the left edge a hand holds up a small transmitter, and across the table an aluminum bar with receivers rests on a clear storage box beside a bench power supply" zoomable=true %}
    <figcaption class="prj-caption">Chasing range spikes (May&nbsp;2020): the <span class="nobr">HG-M40DB</span> transmitter held up by hand at the left, the receiver bar on a storage box across the table. The spikes were reflections, and a 9&nbsp;V drive instead of 12&nbsp;V removed&nbsp;them.</figcaption>
  </figure>
  <figure>
    <video src="{{ '/assets/video/projects/person-following-robot/received-burst-vs-distance-2020-05.mp4' | relative_url }}" poster="{{ '/assets/img/projects/person-following-robot/received-burst-vs-distance-2020-05-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">The received burst (cyan) as the transmitter moves nearer and farther along one bearing (May&nbsp;2020): it shifts in time and grows and shrinks with the&nbsp;distance.</figcaption>
  </figure>
  <figure>
    <video src="{{ '/assets/video/projects/person-following-robot/received-burst-vs-angle-2020-05.mp4' | relative_url }}" poster="{{ '/assets/img/projects/person-following-robot/received-burst-vs-angle-2020-05-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">At one distance, changing the angle leaves the burst in place but changes its size (May&nbsp;2020). A weaker burst takes longer to cross the receiver's ≈174&nbsp;mV threshold, which is how I explained a range error that varied with the&nbsp;angle.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/receiver-can-cut.webp" alt="Four close-ups of an ultrasonic receiver held in fingers: with its mesh and full metal can, front and side, and after the end of the can was cut off, exposing the piezo element" zoomable=true %}
    <figcaption class="prj-caption">A fix that did not pay off (Jun.&nbsp;2020): a receiver before (top) and after (bottom) I cut down its can to let in sound from wider angles. Measured at <span class="nobr">50–200&nbsp;cm</span> and <span class="nobr">0–50°</span>, the ranges moved by <span class="nobr">−0.1 to +1.9&nbsp;cm</span> on average and the angle covered did not&nbsp;grow.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/rf-short-and-long-leads.webp" alt="Left: an nRF24L01+ radio module held in fingers on short jumper wires to a green microcontroller board with an LCD. Right: an nRF24L01+ module on a long gray cable" zoomable=true %}
    <figcaption class="prj-caption">The radio on the bench (Sep.&nbsp;2020): an nRF24L01+ on short leads to an ATmega128 board (left) and on a long cable (right). With the long cable the data came back garbled until I slowed the SPI&nbsp;clock.</figcaption>
  </figure>
</div>

<details class="prj-log">
<summary>Seven more photos and screen captures from&nbsp;2020</summary>
<div class="prj-media prj-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/hc-sr04-grid-marks.webp" alt="Two photos of an HC-SR04 held by hand on grid paper at hand-written distance marks, 25 cm in one and 50 cm in the other" zoomable=true %}
    <figcaption class="prj-caption">Ground truth drawn by hand on grid paper (Apr.&nbsp;2020): the <span class="nobr">HC-SR04</span> held at the 25 and 50&nbsp;cm marks read 24.94 and 49.49&nbsp;cm.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/one-way-first-bench.webp" alt="Two microcontroller development boards on a keyboard, each wired to an HC-SR04 ultrasonic module, one module partly wrapped in tissue" zoomable=true %}
    <figcaption class="prj-caption">A <span class="nobr">one-way</span> test with two <span class="nobr">HC-SR04</span> modules on two ATmega128 boards (Apr.&nbsp;2020): one only sends the burst, the other only listens. The scope confirmed the trigger going&nbsp;out.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/srf02-bench.webp" alt="A microcontroller development board wired to an SRF02 ultrasonic sensor lying on grid paper, with a USB hub and serial and Bluetooth dongles in the foreground" zoomable=true %}
    <figcaption class="prj-caption">The SRF02 under test (Apr.&nbsp;2020): an ATmega128 board commands the sensor over UART and passes each range to the PC over Bluetooth. It read <span class="nobr">15–50&nbsp;cm</span> within 1&nbsp;cm, but 5 and 10&nbsp;cm came back as 12 and 14&nbsp;cm.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/echo-threshold.webp" alt="Three oscilloscope photos: a small and a large received burst against a digital output, and a burst building up toward a dashed cursor at 174 millivolts" zoomable=true %}
    <figcaption class="prj-caption">The threshold behind the <span class="nobr">angle-dependent</span> error (May&nbsp;2020): a large echo crosses the receiver's detection level sooner than a small one (top), and the bottom capture shows an echo just before it grew too weak to register, against the ≈174&nbsp;mV threshold. Beyond 110&nbsp;cm, ranges came in even below that level, so the explanation did not hold&nbsp;everywhere.</figcaption>
  </figure>
</div>
<div class="prj-media">
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/srf02-offset-scope.webp" alt="Two oscilloscope captures of serial command bursts: bursts 10.0 ms apart, and two command bursts 2.29 ms apart" zoomable=true %}
    <figcaption class="prj-caption">Hunting the constant 82&nbsp;cm offset in <span class="nobr">one-way</span> SRF02 ranging (Apr.&nbsp;2020). Left: commands sent 10&nbsp;ms apart in code measured 10.0&nbsp;ms, so the clock was fine. Right: the listen and burst commands went out 2.29&nbsp;ms apart, or 77.86&nbsp;cm of sound&nbsp;travel.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/rf-latency-scope.webp" alt="Two oscilloscope captures of radio traffic: polling pulses 2.73 ms apart against SPI activity, and a 6.01 ms interval from transmit to receive" zoomable=true %}
    <figcaption class="prj-caption">Pinning the radio latency (Sep.&nbsp;2020). Left: one pass of my <span class="nobr">status-polling</span> loop took 2.73&nbsp;ms, so a packet could land anywhere inside it. Right: after I took the debug print out of that loop and checked how payload size adds delay, transmit to receive measured 6.01&nbsp;ms, and it held at <span class="nobr">6.00–6.02&nbsp;ms</span> over&nbsp;<span class="nobr">50–350&nbsp;cm</span>.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/stm32-spi-logic-analyzer.webp" alt="Logic analyzer software decoding SPI: enable, clock, MISO and MOSI channels with byte values, and a table of the decoded transfers" zoomable=true %}
    <figcaption class="prj-caption">Porting the radio driver to the STM32 (Oct.&nbsp;2020): SPI traffic to the nRF24L01+ decoded on a logic analyzer. On the scope, the gap between packets measured 3.06&nbsp;µs; the datasheet asks for at least 50&nbsp;ns of CSN inactive&nbsp;time.</figcaption>
  </figure>
</div>
</details>

## The graduation project (2021)

<figure class="prj-embed">
  <iframe src="https://www.youtube-nocookie.com/embed/_oMrVY5DOvg?rel=0" title="Final demo of the graduation project (YouTube)" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  <figcaption class="prj-caption">Our team's final demo video of the graduation project, a <span class="nobr">construction-site</span> <span class="nobr">material-transport</span> robot with a following function, uploaded to YouTube by a teammate (Oct.&nbsp;2021). My part was the following subsystem described&nbsp;below.</figcaption>
</figure>

- **The team and my part.** The goal was a tracked robot that carries materials up <span class="nobr">construction-site</span> stairs at least 120&nbsp;cm wide, following a worker. We were a team of three. The drive teammate took drive control, the landing gear, <span class="nobr">anti-tilt</span> control and path planning; the third member took the manual remote software, terrain judgment and the cargo bay. I owned the following subsystem: its boards, the ultrasonic and radio localization, the <span class="nobr">receive-range</span> extension and the LiDAR&nbsp;interface.
- **Localization, measured against marked positions.** With two receivers on a bar, <span class="nobr">re-mounting</span> them at an angle brought every point from 0 to 40° at 100 and 150&nbsp;cm within 3.6&nbsp;cm and 2°; before, a target at 30° and 100&nbsp;cm read 120.2&nbsp;cm and 44°. With four receivers, targets at 70&nbsp;cm and 20, 30 and 40° to the side read 19.8, 32.1 and 42.1°, though the 10° point read 1.1°. Vertical localization broke down beyond about 10°: a target 40° up read 90° and&nbsp;178&nbsp;cm.
- **Radio failures handled, then counted.** A target standing at 70&nbsp;cm sometimes read about 210&nbsp;cm. On the scope I timed both failures: ≈3&nbsp;ms when the packet was lost, ≈1.2&nbsp;ms when the acknowledgment was lost. I turned <span class="nobr">auto-retransmit</span> off (15&nbsp;→&nbsp;0), resent after 1&nbsp;ms whenever transmission took longer than 1.5&nbsp;ms, and rejected readings that jumped by more than 70&nbsp;cm. After the fix, each lost packet adds 3&nbsp;ms to the 29&nbsp;ms cycle. A lost acknowledgment still delays the burst by ≈2.5&nbsp;ms (≈85&nbsp;cm of range), so the jump filter drops that reading and the cycle stretches to ≈61&nbsp;ms. Of 519 logged exchanges, 492 succeeded on the first try, 25 lost one packet, 1 lost two in a row and 1 lost the&nbsp;acknowledgment.
- **Dead ends, written down.** A 90° <span class="nobr">wide-angle</span> receiver (<span class="nobr">IUM-D10</span>) gave erratic data with our transmitter. I measured both drives (≈57 vs. ≈3.8&nbsp;Vpp), matched echo amplitudes by distance with a 1.765&nbsp;ms delay, and still got data only at <span class="nobr">25–45&nbsp;cm</span>, so I kept the SRF02 receivers. A DYNAMIXEL receiver tilt was dropped from the plan, though I kept its connectors on the July layout. The first following run in Apr.&nbsp;2021 failed on spikes; the logs put them in the measured motor speeds, while the following unit's commands, sent every 50&nbsp;ms, stayed&nbsp;smooth.

<div class="prj-media prj-media-2">
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/tracked-chassis.webp" alt="Side view of a tracked robot chassis with a raised front track, a battery pack and a vertical mast, on a lab floor" zoomable=true %}
    <figcaption class="prj-caption">The tracked chassis of the graduation project (Jan.&nbsp;2021). My part was the unit that tells it where the worker&nbsp;is.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/receiver-remount-before-after.webp" alt="Seminar slide: a sketch and photo of receivers mounted at an angle under a bar, and two tables of true and measured distance and angle before and after the change" zoomable=true %}
    <figcaption class="prj-caption">Two receivers on a bar, before (top table) and after (bottom) I <span class="nobr">re-mounted</span> them at an angle (Feb.&nbsp;2021). After: every point from 0 to 40° at 100 and 150&nbsp;cm within 3.6&nbsp;cm and 2°. Before: 40° at 100&nbsp;cm gave no reading at&nbsp;all.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/localization-rig.webp" alt="An aluminum frame with four ultrasonic receivers on its two sides, two at each height, and a hand-drawn 10 cm grid board with labeled coordinates" zoomable=true %}
    <figcaption class="prj-caption">The <span class="nobr">four-receiver</span> frame, 45&nbsp;cm wide with receivers 20&nbsp;cm apart vertically, and the <span class="nobr">hand-drawn</span> 10&nbsp;cm grid board that gave the true target positions in the tests at 120 and 200&nbsp;cm (May&nbsp;2021).</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/ack-loss-before-after.webp" alt="Seminar slide: a sketch of the robot's receiver and the handheld transmitter, each with a radio module, and two plots of range over time, with two spikes to about 210 cm before the fix and none after" zoomable=true %}
    <figcaption class="prj-caption">Range of a target standing at about 70&nbsp;cm, before and after I handled lost acknowledgments (Feb.&nbsp;2021): the ≈210&nbsp;cm spikes are gone. Left: the scheme, a radio message that announces the burst and a receiver that times&nbsp;it.</figcaption>
  </figure>
</div>

### In the lab

Phone clips, photos, scope captures and charts from the graduation project's&nbsp;seminars.

<div class="prj-media prj-media-2">
  <figure>
    <video src="{{ '/assets/video/projects/person-following-robot/rf-latency-irregular-2021-01.mp4' | relative_url }}" poster="{{ '/assets/img/projects/person-following-robot/rf-latency-irregular-2021-01-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">Radio timing on the scope (Jan.&nbsp;2021): the latency jumped from one exchange to the next and held steady, at <span class="nobr">1.346–1.355&nbsp;ms</span>, only when it was shortest. Tracing why led to the <span class="nobr">lost-packet</span> handling a week&nbsp;later.</figcaption>
  </figure>
  <figure>
    <video src="{{ '/assets/video/projects/person-following-robot/following-run-bench-2021-04.mp4' | relative_url }}" poster="{{ '/assets/img/projects/person-following-robot/following-run-bench-2021-04-poster.webp' | relative_url }}" autoplay loop muted playsinline controls preload="metadata"></video>
    <figcaption class="prj-caption">A following run in the lab (Apr.&nbsp;2021), cropped to the robot: it stays in place, tethered by cables, while its tracks run, change speed and stop; the person holding the target is out of frame. The logs shown with this clip put my following unit's speed commands between about 4 and 13&nbsp;cm/s; the drive teammate's controller ran the motors, whose measured speeds show&nbsp;spikes.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/localization-scatter-200cm.webp" alt="Four scatter plots in centimeters, each with blue estimated positions and an orange true position: a target 50 cm to the left, 50 cm to the right, 30 cm up and 30 cm down" zoomable=true %}
    <figcaption class="prj-caption">Estimated target positions (blue) against the true one (orange), 200&nbsp;cm from the robot (May&nbsp;2021): targets 50&nbsp;cm left and right (top) and 30&nbsp;cm up and down (bottom), with <span class="nobr">left–right</span> across and <span class="nobr">up–down</span> vertically, in cm. For the side targets the <span class="nobr">left–right</span> error stayed within about 12&nbsp;cm, but the target 30&nbsp;cm up read <span class="nobr">35–59&nbsp;cm</span>&nbsp;up.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/following-envelope.webp" alt="Two closed curves on a centimeter grid: the target positions rated followable at 200 cm in blue and at 120 cm in orange" zoomable=true %}
    <figcaption class="prj-caption">The following envelope in my Jul.&nbsp;2021 summary, drawn after the <span class="nobr">grid-board</span> tests: the target positions it rates as followable span about 55&nbsp;cm left to 59&nbsp;cm right and 30&nbsp;cm down to 20&nbsp;cm up at 200&nbsp;cm (blue), and 49&nbsp;cm left to 40&nbsp;cm right and 20&nbsp;cm down to 12&nbsp;cm up at 120&nbsp;cm&nbsp;(orange).</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/element-swaps.webp" alt="Left: a stock HC-SR04 next to one whose receiver was replaced by a different transducer with a golden mesh. Right: a black transducer fitted in place of an HC-SR04's transmitter, held in fingers" zoomable=true %}
    <figcaption class="prj-caption">Swapping transducer elements to widen the receive range (<span class="nobr">Jan.–Feb.&nbsp;2021</span>). Left: a stock <span class="nobr">HC-SR04</span> and one whose receiver I replaced with a TS601 element, which gave no correct data from 45&nbsp;cm on. Right: a V40AW18B in place of the transmitter. The lesson I recorded: an element works only with a drive that matches its&nbsp;specs.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/ir-sensor-calibration.webp" alt="Chart of distance in centimeters against sensor output voltage: 14 measured points from 20 to 150 cm on a falling curve, with a dotted power-law fit" zoomable=true %}
    <figcaption class="prj-caption">Calibrating the GP2Y0A02YK0F infrared distance sensor, planned for obstacle and stair detection (Feb.&nbsp;2021): distance against output voltage at 14 points over <span class="nobr">20–150&nbsp;cm</span>, with the fit <span class="nobr">d&nbsp;=&nbsp;72.935·V<sup>−1.249</sup></span> (dotted). In firmware I interpolated linearly between the&nbsp;points.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/drive-and-echo-matching.webp" alt="Four oscilloscope captures: a large drive waveform of about 57 V peak to peak, a small 3.8 V drive, and two received echo bursts of 105 and 108 mV" zoomable=true %}
    <figcaption class="prj-caption">Testing a 90° <span class="nobr">wide-angle</span> receiver (May&nbsp;2021). Top: our <span class="nobr">HG-M40DB</span> transmitter drives at ≈57&nbsp;Vpp, the <span class="nobr">IUM-D10</span> at ≈3.8&nbsp;Vpp. Bottom: at an <span class="nobr">IUM-D10</span> receiver, an <span class="nobr">IUM-D10</span> at 30&nbsp;cm and the <span class="nobr">HG-M40DB</span> at 90&nbsp;cm gave matching echoes of 105 and 108&nbsp;mV, yet even with a 1.765&nbsp;ms delay to make up the 60&nbsp;cm, data came only at&nbsp;<span class="nobr">25–45&nbsp;cm</span>.</figcaption>
  </figure>
  <figure>
    {% include figure.liquid path="assets/img/projects/person-following-robot/rf-loss-timing.webp" alt="Two oscilloscope captures of the radio handshake, one with cursors 2.976 ms apart and one with cursors 1.184 ms apart" zoomable=true %}
    <figcaption class="prj-caption">Radio failures timed on the scope (Feb.&nbsp;2021): about 3&nbsp;ms when the packet was lost (top, cursors 2.976&nbsp;ms apart) and about 1.2&nbsp;ms when the acknowledgment was lost (bottom,&nbsp;1.184&nbsp;ms).</figcaption>
  </figure>
</div>

## Debugging log

Some of the faults I tracked down, and how I found them.

<div class="prj-table-wrap prj-debug"><table><thead><tr><th>When</th><th>Symptom</th><th>How I found it</th><th>Fix</th></tr></thead><tbody>
<tr><td data-label="When">Apr.&nbsp;2020</td><td data-label="Symptom"><span class="nobr">One-way</span> SRF02 ranges read <span class="nobr">81.8–82.9&nbsp;cm</span> too far at every&nbsp;distance</td><td data-label="How I found it">Confirmed on the scope that the MCU's clock was fine, then timed the gap between the listen and burst commands: 2.29&nbsp;ms, or 77.86&nbsp;cm of sound&nbsp;travel.</td><td data-label="Fix">Subtracted it. The <span class="nobr">3.9–5.0&nbsp;cm</span> residual, and a 10&nbsp;ms delay that moved readings by 260 instead of 340&nbsp;cm, stayed open&nbsp;questions.</td></tr>
<tr><td data-label="When">May&nbsp;2020</td><td data-label="Symptom">Range spikes during fast motion that an RC <span class="nobr">low-pass</span> and a median filter could not&nbsp;remove</td><td data-label="How I found it">Checked a <span class="nobr">frequency-shift</span> idea on the scope, traced the spikes to reflections, then swept drive voltage against acceptance&nbsp;angle.</td><td data-label="Fix">Drove the transmitter at 9&nbsp;V (12&nbsp;V spiked even standing still) and dropped the median filter, which only added&nbsp;lag.</td></tr>
<tr><td data-label="When">Aug.&nbsp;2020</td><td data-label="Symptom">My handheld board: the <span class="nobr">ST-LINK</span> would not attach, and the 3.3&nbsp;V rail read 2.8&nbsp;V</td><td data-label="How I found it">Read the datasheets: the probe needs target VCC on its header, and the LM1117 needs at least 4.75&nbsp;V from a 3.8&nbsp;V&nbsp;battery.</td><td data-label="Fix">A bodge wire from MCU_VDD to the ISP header, and an AME8801AEEV <span class="nobr">low-dropout</span> regulator instead of the&nbsp;LM1117.</td></tr>
<tr><td data-label="When">Sep.&nbsp;2020</td><td data-label="Symptom">Radio latency at 50&nbsp;cm varied from 9.5 to 10.5&nbsp;ms</td><td data-label="How I found it">On the scope, one pass of the <span class="nobr">status-polling</span> loop, which also formatted a debug string and sent it over UART, took 2.73&nbsp;ms; a packet could arrive anywhere in that&nbsp;window.</td><td data-label="Fix">Took the debug print out of the loop and checked how payload size adds delay. Latency then held at <span class="nobr">6.00–6.02&nbsp;ms</span> over <span class="nobr">50–350&nbsp;cm</span>, applied as a constant 6.01&nbsp;ms&nbsp;offset.</td></tr>
<tr><td data-label="When">Jan.&nbsp;2021</td><td data-label="Symptom">The radio worked between my own STM32F405 boards but stayed silent on a&nbsp;<span class="nobr">NUCLEO-F429ZI</span></td><td data-label="How I found it">Matched the timing, fixed a <span class="nobr">CRC-length</span> difference, unified the SPI read routine, checked the radio's registers one by one, then followed the datasheet's receive&nbsp;flowchart.</td><td data-label="Fix">CE was never raised; driving it high made the F429 receive. Why my F405 boards had received without it stayed an open&nbsp;question.</td></tr>
<tr><td data-label="When">Feb.&nbsp;2021</td><td data-label="Symptom">A target standing at 70&nbsp;cm sometimes read about 210&nbsp;cm</td><td data-label="How I found it">Timed the radio handshake on the scope: ≈3&nbsp;ms when the packet was lost, ≈1.2&nbsp;ms when the acknowledgment was&nbsp;lost.</td><td data-label="Fix"><span class="nobr">Auto-retransmit</span> 15&nbsp;→&nbsp;0, a resend after 1&nbsp;ms and a 70&nbsp;cm jump filter, checked over 519 logged&nbsp;exchanges.</td></tr>
<tr><td data-label="When">May&nbsp;2021</td><td data-label="Symptom">A 90° <span class="nobr">wide-angle</span> receiver gave erratic&nbsp;data</td><td data-label="How I found it">Measured both drives (≈57 vs. ≈3.8&nbsp;Vpp) and matched echo amplitudes by distance with a 1.765&nbsp;ms&nbsp;delay.</td><td data-label="Fix">It worked only at <span class="nobr">25–45&nbsp;cm</span>, so I recorded a dead end and kept the SRF02&nbsp;receivers.</td></tr>
</tbody></table></div>

## Seminar log

{% capture log_summary %}All {{ sessions.size }} seminars, <span class="nobr">Mar.&nbsp;2020 – Jul.&nbsp;2021</span>{% endcapture %}
{% include prj_log.liquid sessions=sessions summary=log_summary %}

<div class="prj-ko" lang="ko">
<p><strong>한국어 요약</strong></p>
<p>2020년&nbsp;3월부터 2021년&nbsp;10월까지 사람을 따라가는 로봇의 추종부를 맡았습니다. 사람이 든 송신기가 초음파를 쏘는 순간을 RF로 알려 주면, 로봇의 수신기가 단방향 비행시간으로 거리와 방향을 구하는 방식입니다. RF 통신의 지연 시간과 송수신 센서 간 동기화까지 고려해 사람의 위치를 정밀하게 추정했고, 이를 바탕으로 정확한 추종 시스템을 구현했습니다. 2020년에는 이 추종부가 제 개인 과제였고, STM32F405 보드 두&nbsp;장을 OrCAD로 설계하고, 제작된 기판에 부품을 직접 납땜해 조립한 뒤 브링업까지 했습니다. 2021년에는 3명이 함께한 졸업작품에서 건설 현장용 자재 운반 로봇의 추종 시스템을 맡아 보드 세&nbsp;장을 더 설계하고 직접&nbsp;제작했습니다.</p>
<p>결과는 실측과 비교해 확인했습니다. 바닥에 깐 종이와 10&nbsp;cm 격자판 위에서 목표 위치를 정하고 오실로스코프로 타이밍을 쟀으며, 수신기를 비스듬히 다시 단 뒤에는 100·150&nbsp;cm에서 <span class="nobr">0–40°</span> 전 구간이 거리 3.6&nbsp;cm, 각도 2°&nbsp;이내로 들어왔습니다. 무선 패킷 손실 처리는 519회 교환으로 확인했고(첫 시도 성공 492회), 문제는 필터로 덮기보다 반사파, 폴링 루프 안의 디버그 출력, 올라가지 않은 CE 핀처럼 원인을 찾아 고쳤습니다. 90° 광각 수신기 실패와 10°&nbsp;이상에서 무너진 상하 위치 추정처럼 막힌 길도 그대로&nbsp;기록했습니다.</p>
</div>

{% include prj_more.liquid %}
