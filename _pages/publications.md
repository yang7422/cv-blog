---
layout: page
permalink: /publications/
title: publications
description: Under review, peer-reviewed publications, and patents. * marks equal contribution.
nav: true
nav_order: 1
---

<!-- _pages/publications.md -->
<!-- Keep `description` plain text: it is copied into <meta name="description">, so HTML with quotes breaks the head. -->

<p class="venue-legend">
  Badge colors —
  <span style="color:#1e40af">■</span> journal ·
  <span style="color:#047857">■</span> conference ·
  <span style="color:#b45309">■</span> workshop ·
  <span style="color:#6d28d9">■</span> domestic (Korea) ·
  <span style="color:#64748b">■</span> under review ·
  <span style="color:#9f1239">■</span> patent
</p>

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="publications">

<h2 class="bibliography">Under Review</h2>

{% bibliography --file under_review --group_by none %}

<h2 class="bibliography">Peer-Reviewed Publications</h2>

{% bibliography %}

<h2 class="bibliography">Patents</h2>

{% bibliography --file patents --group_by none %}

</div>
