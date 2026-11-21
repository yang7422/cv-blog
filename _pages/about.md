---
layout: about
title: about
permalink: /
# Line breaks: each <span class="nobr"> stays on one line (_sass/_custom.scss), so a
# line can only break at a normal space between two spans. &nbsp; before "·" keeps
# the dot from starting a line.
subtitle: >-
  <span class="nobr">Integrated M.S.–Ph.D. Student</span>&nbsp;· <span class="nobr">SPARO Lab, Inha University</span>&nbsp;·
  <span class="nobr">Robust Perception &amp;</span> <span class="nobr">Robust State Estimation</span>

profile:
  align: right
  image: geonmo_yang.jpg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p><span class="nobr">SPARO Lab</span> <span class="nobr">(Spatial AI &amp; Robotics)</span></p>
    <p class="nobr">Inha University</p>
    <p><span class="nobr">Incheon,</span> <span class="nobr">Republic of Korea</span></p>

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: true # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 6 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false # re-enable once the blog has posts
  scrollable: true
  limit: 3
---

Hi, I'm **Geonmo Yang** (양건모), an integrated M.S.–Ph.D. student at [SPARO Lab](https://sparolab.github.io/) (Spatial AI & Robotics Lab), Inha University, advised by Prof. Younggun Cho.

I build **robust perception** and **robust state estimation** for robots that have to keep working when sensing conditions break down — turbid water, haze, marine snow, sparse or biased depth, and environments that keep changing over time.

**Research focus**

- **Robust perception** — underwater image enhancement, depth estimation and completion, and uncertainty estimation under scattering and sparse, spatially biased measurements. _(Joint-ID, TRIDENT, PGSPN)_
- **Robust state estimation** — LiDAR SLAM, localization, and long-term map maintenance in changing environments, from industry R&D to multi-robot field deployments. _(Time-Integrated Occupancy, SKiD-SLAM, Commerge, KISS-IMU)_

{% assign own_talks = site.data.ihlab_seminars | where_exp: "s", "s.project != 'rails'" %}

**Highlights**

- 3 first-author journal papers (IEEE Sensors Journal ×2, MDPI Sensors) and co-authored papers in IJRR, IEEE T-FR, RA-L, and ICRA
- 2 registered Korean patents — underwater image enhancement & depth estimation, and sensor-fusion image dehazing
- 2nd place out of 131 teams, IMU Odometry Challenge @ IROS 2026
- Silver Prize, 32nd Samsung HumanTech Paper Award (2026)&nbsp;· Grand Prize, Graduate Research Award, Inha University (2026)
- Research internship at Riibotics (robust LiDAR SLAM & localization)&nbsp;· international collaborations with Stevens Institute of Technology and MIT&nbsp;· industry project with Hyundai E&C
- Undergraduate research at IHLAB, Tech University of Korea: four hands-on projects, from <span class="nobr">register-level</span> firmware to circuit boards I designed and brought up, and {{ own_talks.size }} weekly lab seminars ([projects]({{ '/projects/' | relative_url }}))

🇰🇷 [한국어 소개 페이지]({{ '/ko/' | relative_url }})

{% include glue_words.liquid %}
