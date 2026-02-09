"""
Computer Lab: Pi Precision Analysis - Surface Area of Sphere
Formula: A = 4πr²
This program calculates errors AND generates visualization graphs
"""

from mpmath import mp
import matplotlib.pyplot as plt
import numpy as np

# Set high precision
mp.dps = 150

def calculate_surface_area(r, pi_value):
    """Calculate surface area of sphere: A = 4 * pi * r^2"""
    return 4 * pi_value * r * r

def truncate_pi(decimals):
    """Truncate pi to specified decimal places"""
    pi_str = str(mp.pi)
    dot_index = pi_str.index('.')
    truncated = pi_str[:dot_index + decimals + 1]
    return mp.mpf(truncated)

def round_pi(decimals):
    """Round pi to specified decimal places"""
    return mp.mpf(round(mp.pi, decimals))

# Test with radius = 10 meters
r = 10

# Calculate true surface area with full precision
true_pi = mp.pi
true_area = calculate_surface_area(r, true_pi)

print("=" * 70)
print("SURFACE AREA CALCULATION ERROR ANALYSIS")
print("Formula: A = 4πr²")
print(f"Radius: {r} meters")
print("=" * 70)
print(f"\nTrue Surface Area (full precision): {true_area} m²\n")

# Test at required decimal places
decimal_places = [20, 40, 60, 100]

print("=" * 70)
print("ERRORS AT DIFFERENT DECIMAL PLACES")
print("=" * 70)

errors_truncated = []
errors_rounded = []

for decimals in decimal_places:
    print(f"\n{decimals} DECIMAL PLACES:")
    print("-" * 70)
    
    # Truncated
    pi_truncated = truncate_pi(decimals)
    area_truncated = calculate_surface_area(r, pi_truncated)
    error_truncated = abs(true_area - area_truncated)
    errors_truncated.append(float(error_truncated))
    
    # Rounded
    pi_rounded = round_pi(decimals)
    area_rounded = calculate_surface_area(r, pi_rounded)
    error_rounded = abs(true_area - area_rounded)
    errors_rounded.append(float(error_rounded))
    
    print(f"Truncation Error: {error_truncated} m²")
    print(f"Rounding Error:   {error_rounded} m²")
    
    # Show which is better
    if error_rounded < error_truncated:
        print(f"→ Rounding is MORE accurate")
    elif error_truncated < error_rounded:
        print(f"→ Truncation is MORE accurate")
    else:
        print(f"→ Both methods have equal error")

print("\n" + "=" * 70)
print("GENERATING VISUALIZATIONS...")
print("=" * 70)

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Pi Precision Analysis: Truncation vs Rounding\nUsing Surface Area of Sphere (A = 4πr²)', 
             fontsize=16, fontweight='bold')

# Plot 1: Error comparison (log scale)
ax1 = axes[0, 0]
ax1.semilogy(decimal_places, errors_truncated, 'o-', label='Truncation', 
             linewidth=2, markersize=8, color='red', alpha=0.7)
ax1.semilogy(decimal_places, errors_rounded, 's-', label='Rounding', 
             linewidth=2, markersize=8, color='blue', alpha=0.7)
ax1.set_xlabel('Number of Decimal Places', fontsize=11, fontweight='bold')
ax1.set_ylabel('Absolute Error (m²)', fontsize=11, fontweight='bold')
ax1.set_title('Error in Surface Area Calculation', fontsize=12, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Plot 2: Bar chart comparison
ax2 = axes[0, 1]
x = np.arange(len(decimal_places))
width = 0.35
bars1 = ax2.bar(x - width/2, errors_truncated, width, label='Truncation', 
                color='red', alpha=0.7)
bars2 = ax2.bar(x + width/2, errors_rounded, width, label='Rounding', 
                color='blue', alpha=0.7)
ax2.set_xlabel('Decimal Places', fontsize=11, fontweight='bold')
ax2.set_ylabel('Absolute Error (m²)', fontsize=11, fontweight='bold')
ax2.set_title('Direct Error Comparison', fontsize=12, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(decimal_places)
ax2.legend(fontsize=11)
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3, axis='y')

# Plot 3: Error difference
ax3 = axes[1, 0]
error_differences = [abs(t - r) for t, r in zip(errors_truncated, errors_rounded)]
ax3.semilogy(decimal_places, error_differences, 'o-', linewidth=2.5, 
             markersize=8, color='purple', alpha=0.7)
ax3.set_xlabel('Number of Decimal Places', fontsize=11, fontweight='bold')
ax3.set_ylabel('|Error_truncated - Error_rounded|', fontsize=11, fontweight='bold')
ax3.set_title('Absolute Difference Between Methods', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3)

# Plot 4: Which method is better?
ax4 = axes[1, 1]
better_method = []
colors_list = []
for t, r in zip(errors_truncated, errors_rounded):
    if t < r:
        better_method.append(1)  # Truncation wins
        colors_list.append('red')
    elif r < t:
        better_method.append(2)  # Rounding wins
        colors_list.append('blue')
    else:
        better_method.append(0)  # Tie
        colors_list.append('gray')

bars = ax4.bar(decimal_places, better_method, color=colors_list, alpha=0.7, width=8)
ax4.set_xlabel('Decimal Places', fontsize=11, fontweight='bold')
ax4.set_ylabel('Better Method', fontsize=11, fontweight='bold')
ax4.set_title('Which Method is More Accurate?', fontsize=12, fontweight='bold')
ax4.set_yticks([1, 2])
ax4.set_yticklabels(['Truncation', 'Rounding'])
ax4.grid(True, alpha=0.3, axis='y')

# Add legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='red', alpha=0.7, label='Truncation Better'),
                   Patch(facecolor='blue', alpha=0.7, label='Rounding Better')]
ax4.legend(handles=legend_elements, fontsize=10)

plt.tight_layout()
plt.savefig('pi_error_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Graph saved as 'pi_error_analysis.png'")

# Create second visualization showing pi digits
fig2, ax = plt.subplots(figsize=(14, 6))
pi_str = str(mp.pi)[2:]  # Remove "3."

positions = [20, 40, 60, 100]
digits_to_show = 110
digits = [int(d) for d in pi_str[:digits_to_show]]

colors_list = ['lightblue'] * digits_to_show
for pos in positions:
    if pos <= digits_to_show:
        colors_list[pos-1] = 'orange'

x_vals = list(range(1, len(digits) + 1))
bars = ax.bar(x_vals, digits, color=colors_list, edgecolor='black', linewidth=0.5)

# Annotate key positions
for pos in positions:
    if pos <= digits_to_show:
        digit = digits[pos-1]
        ax.annotate(f'{pos}th: {digit}', 
                   xy=(pos, digit), 
                   xytext=(pos, digit + 2),
                   ha='center',
                   fontsize=10,
                   fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.8),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=1.5))

ax.set_xlabel('Decimal Position', fontsize=12, fontweight='bold')
ax.set_ylabel('Digit Value', fontsize=12, fontweight='bold')
ax.set_title('First 110 Decimal Digits of Pi\n(Highlighted: 20th, 40th, 60th, 100th positions)', 
            fontsize=14, fontweight='bold')
ax.set_ylim(0, 12)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('pi_digits.png', dpi=300, bbox_inches='tight')
print("✓ Graph saved as 'pi_digits.png'")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)
print("Is there a difference between truncation and rounding?")
print("YES - but at high decimal precision, both become extremely accurate.")
print("The visualizations show how errors decrease as precision increases.")
print("=" * 70)
print("\nAll done! Check the generated images.")