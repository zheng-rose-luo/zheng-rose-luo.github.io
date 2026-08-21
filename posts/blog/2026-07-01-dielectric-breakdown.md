---
title: Dielectric Breakdown Toughness
date: 2026-07-01
excerpt: Proposing a new material parameter bridging defect size and insulation performance.
---

# Dielectric Breakdown Toughness

## Introduction

The electrical J-integral is defined as:

$$J_e = \int_{\Gamma} (W_e \, dy - \mathbf{T} \cdot \frac{\partial \mathbf{D}}{\partial x} \, ds)$$

For a dielectric material, the breakdown condition can be expressed as:

$$K_{e} = Y \sqrt{\pi a}$$

where $K_e$ is the electrical stress intensity factor, $Y$ is a geometric factor, and $a$ is the defect size.

## Defect Tolerance Hypothesis

We propose that the breakdown strength of a dielectric material is governed by the largest defect:

$$\sigma_b = \frac{K_{ec}}{Y \sqrt{\pi a_{\text{max}}}}$$

where $K_{ec}$ is the **electrical breakdown toughness** - a new material constant.

## Experimental Validation

We fabricated specimens with controlled artificial defects:

| Defect type | Size range | Material |
|-------------|------------|----------|
| Notch | 1-10 μm | PDMS |
| Hole | 100 nm - 1 μm | Silicone |
| Crack | 10-100 μm | Polyurethane |

The Weibull distribution confirms:

$$P_f = 1 - \exp\left[-\left(\frac{\sigma}{\sigma_0}\right)^m\right]$$

where $m$ is the Weibull modulus.

## Conclusion

This work establishes electrical breakdown toughness as a meaningful material parameter, bridging fracture mechanics and dielectric physics.