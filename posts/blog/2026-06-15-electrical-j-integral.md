---
title: Checking an Electrical Growth-Force Calculation
date: 2026-06-15
updated: 2026-11-24
excerpt: How energy changes and integral calculations provide complementary checks on a model of conducting-channel growth.
tags: Electrical failure · Numerical modelling · Research methods
---

# Checking an Electrical Growth-Force Calculation

A conducting channel concentrates the electric field near its tip. A sharper tip can produce a larger local field, but that observation alone does not specify the energy available for the channel to grow. The growth-driving force also depends on the specimen, loading and prescribed change in channel geometry.

This distinction is central to my theoretical work on electrical failure.

## Define the change before calculating its cost

To calculate a growth-driving force, I first need to specify what advances. Extending a channel, moving its conducting head and changing its tip shape are different geometrical operations. A meaningful comparison between calculations must use the same prescribed change and electrical boundary conditions.

In my current formulation, energy changes, boundary integrals and domain integrals provide different ways to calculate the force associated with a specified advance. Their agreement supplies a numerical consistency check. The assumptions under which an integral is independent of the chosen path are part of the derivation.

## What the numerical checks establish

I compare the formulations in two- and three-dimensional geometries. Relevant checks include mesh refinement, the choice of integration region and the increment used to approximate an energy change. Agreement is informative only when these calculations represent the same physical boundary-value problem.

The current analysis also examines when mechanical deformation changes the electrical growth force. The comparison follows a selected equilibrium branch; assessing its stability is a separate question.

## Connecting the calculation to failure

I have also implemented phase-field models of breakdown-path evolution in COMSOL. A path-evolution model and an energetic calculation address connected questions, but agreement within a model is only one stage of validation.

The experimental task is to determine whether a proposed resistance criterion predicts measured breakdown across controlled geometries and conditions. This requires reproducible specimens and a clear connection between the quantity calculated and the event measured.

[Read the electrical-failure project](../projects/dielectric-breakdown-theory.html).

