---
layout: about
title: 한국어
permalink: /ko/
nav: true
nav_order: 9
# Line breaks: same <span class="nobr"> scheme as _pages/about.md.
subtitle: >-
  <span class="nobr">인하대학교 SPARO 연구실</span> <span class="nobr">석박사 통합과정</span>&nbsp;·
  <span class="nobr">강건한 인지 &amp;</span> <span class="nobr">강건한 상태 추정</span>

profile:
  align: right
  image: geonmo_yang.jpg
  image_circular: false
  more_info: >
    <p><span class="nobr">SPARO 연구실</span> <span class="nobr">(Spatial AI &amp; Robotics)</span></p>
    <p><span class="nobr">인하대학교</span> <span class="nobr">전기컴퓨터공학과</span></p>
    <p class="nobr">인천, 대한민국</p>

selected_papers: true
social: true

announcements:
  enabled: true
  scrollable: true
  limit: 6

latest_posts:
  enabled: false
---

안녕하세요, 인하대학교 [SPARO 연구실](https://sparolab.github.io/)(지도교수: 조영근)에서 석박사 통합과정 중인 **양건모**입니다.

물속의 탁도·산란·마린 스노우, 듬성듬성하고 한쪽으로 치우친 깊이 측정, 시간이 지나며 바뀌는 환경처럼 **센서 조건이 나빠지는 상황에서도 로봇이 제대로 보고(강건한 인지), 자기 위치를 잃지 않도록(강건한 상태 추정)** 하는 기술을 연구합니다.

**연구 분야**

- **강건한 인지 (Robust Perception)** — 수중 영상 개선, 깊이 추정 및 깊이 보완(depth completion), 불확실성 추정 _(Joint-ID, TRIDENT, PGSPN)_
- **강건한 상태 추정 (Robust State Estimation)** — LiDAR SLAM, 위치 인식, 변화하는 환경에서의 장기 지도 유지 _(Time-Integrated Occupancy, SKiD-SLAM, Commerge, KISS-IMU)_

**주요 성과**

- **논문** — SCIE 1저자 3편(IEEE Sensors Journal 2편, MDPI Sensors 공동 1저자), 공저 IJRR&nbsp;· IEEE T-FR&nbsp;· RA-L&nbsp;· ICRA 등, 국내 학술지(제어로봇시스템학회 논문지) 공동 1저자 1편
- **특허 (등록 2건)** — 수중 영상 강건화 및 거리 정보 추정 시스템(제10-2928592호), 센서 융합을 통한 영상 디헤이징 시스템(제10-2673404호)
- **수상** — IROS 2026 IMU Odometry Challenge 2위(131팀 중), 제32회 삼성휴먼테크 논문대상 은상(2026), 인하대학교 대학원 연구상 대상(2026)&nbsp;· 연구발표상 장려상(2026)&nbsp;· 우수연구상(2024, 학술지 게재), 한국ITS학회 춘계학술대회 우수논문상(2025), 제20회 임베디드 소프트웨어 경진대회 산학 프로젝트 부문 우수상(2022,&nbsp;한국정보처리학회)
- **경력&nbsp;· 협업** — Riibotics 연구 인턴(강건한 LiDAR SLAM&nbsp;· 위치 인식 연구), 미국 Stevens Institute of Technology&nbsp;· MIT 국제 공동연구, 현대건설 산학 과제

{% assign own_talks = site.data.ihlab_seminars | where_exp: "s", "s.project != 'rails'" %}

**이력 요약**

- **2022.03 – 현재**&nbsp;· 인하대학교 전기컴퓨터공학과 석박사 통합과정 (SPARO 연구실)
- **2024.09 – 2025.02**&nbsp;· Riibotics(구 TIM Robotics) 기업부설연구소 연구 인턴 — 강건한 LiDAR SLAM 및 위치 인식 연구, 모바일 로봇 자율주행 소프트웨어 개발
- **2019.03 – 2022.01**&nbsp;· 한국공학대학교 IHLAB 학부연구생 — 펌웨어(ATmega128&nbsp;· STM32), 회로·PCB 설계, 다이나믹셀 다리 로봇, 모터 동기 제어, 사람 추종 로봇. 거의 매주 랩 세미나 {{ own_talks.size }}회 ([프로젝트]({{ '/projects/' | relative_url }}))

<!-- Note: a markdown table here pushes the whole text block below the profile photo (min-content too wide), so keep this a list. -->

전체 논문은 [publications]({{ '/publications/' | relative_url }}), 상세 이력은 [CV]({{ '/cv/' | relative_url }})(영문)에서 볼 수 있습니다.

🇺🇸 [English]({{ '/' | relative_url }})

{% include glue_words.liquid %}
