---
title: Electrical J-Integral & Phase-Field Simulation
date: 2026-06-15
excerpt: Rigorous derivation and COMSOL verification of path-independence.
---

# Electrical J-Integral & Phase-Field Simulation

## Background

The J-integral is a fundamental concept in fracture mechanics. Its electrical analog can be derived from Maxwell's equations.

## Derivation

Starting from the energy-momentum tensor:

$$T_{ij} = W_e \delta_{ij} - E_i D_j$$

The electrical J-integral is:

$$J_e = \int_{\Gamma} (W_e \, dy - \mathbf{T} \cdot \frac{\partial \mathbf{D}}{\partial x} \, ds)$$

## Phase-Field Model

The phase-field evolution equation:

$$\tau \frac{\partial \phi}{\partial t} = 2(1-\phi) \cdot \text{drive} - \text{energy} \cdot \phi$$

where $\phi$ is the phase-field order parameter.

## COMSOL Implementation

We implemented the phase-field model in COMSOL Multiphysics using the PDE interface. Path-independence was verified for multiple integration contours.

## Results

The simulation results show that the electrical J-integral is indeed path-independent, validating our theoretical framework.