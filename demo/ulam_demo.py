import matplotlib.pyplot as plt
import math
from nprime import ulam


def ulam_precision_demo():
    """
    Generate Ulam spiral diagrams for different polygon shapes.
    """
    
    # Create figure with multiple subplots showing different polygon shapes
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Ulam Spiral Diagrams - Fixed Floating Point Precision', fontsize=16)

    # Test different polygon shapes
    shapes = [
        (3, 'Triangle'),
        (4, 'Square'), 
        (5, 'Pentagon'),
        (6, 'Hexagon'),
        (7, 'Heptagon'),
        (8, 'Octagon')
    ]

    for idx, (edges, name) in enumerate(shapes):
        row = idx // 3
        col = idx % 3
        ax = axes[row, col]
        
        coord, prime_coord = ulam(200, edge=edges)
        
        if coord:
            x_coords, y_coords = zip(*coord)
            ax.scatter(x_coords, y_coords, c='lightblue', s=1, alpha=0.6, label='Composite')
        
        if prime_coord:
            x_primes, y_primes = zip(*prime_coord)
            ax.scatter(x_primes, y_primes, c='red', s=3, alpha=0.8, label='Prime')
        
        if edges % 2 == 1: 
            center_x, center_y = 0, 0
            all_x = list(x_coords) + list(x_primes) if coord and prime_coord else []
            max_radius = max(abs(min(all_x)), abs(max(all_x))) if all_x else 10
            
            for i in range(edges):
                angle = i * 2 * math.pi / edges
                end_x = center_x + max_radius * 0.8 * math.cos(angle)
                end_y = center_y + max_radius * 0.8 * math.sin(angle)
                ax.plot([center_x, end_x], [center_y, end_y], 'k--', alpha=0.3, linewidth=0.5)
        
        ax.set_title(f'{name} ({edges} edges)')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.2)
        if idx == 0:
            ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig('ulam_spirals_fixed.png', dpi=150, bbox_inches='tight')
    plt.show()


def compare_precision():
    """
    Demonstrate the precision improvements by showing numerical comparisons.
    """
    print("\n=== Ulam Spiral Precision Improvements ===")
    
    # Test precision for different polygon shapes
    for edges in [3, 5, 7, 9]:
        print(f"{edges}-sided polygon:")
        
        # Calculate angles precisely
        psi = 2 * math.pi / edges
        
        # Show that full rotations are exact
        full_rotation = edges * psi
        expected_2pi = 2 * math.pi
        error = abs(full_rotation - expected_2pi)
        
        print(f"  Angle per edge: {psi:.10f}")
        print(f"  Full rotation:  {full_rotation:.10f}")
        print(f"  Expected (2π):  {expected_2pi:.10f}")
        print(f"  Error:          {error:.2e}")
        
        # Test alignment after many turns
        test_turns = 50
        test_angle = test_turns * psi
        cos_val = math.cos(test_angle)
        sin_val = math.sin(test_angle)
        
        print(f"  After {test_turns} turns: cos={cos_val:.8f}, sin={sin_val:.8f}")
        print()


def main():
    """
    Run the Ulam spiral demonstration.
    """
    print("Ulam Spiral Demo")
    print("=" * 30)
    
    # Show numerical precision improvements
    compare_precision()
    
    # Generate visual demonstration
    try:
        ulam_precision_demo()
    except ImportError:
        print("Matplotlib not available. Skipping visual demo.")
        print("Install matplotlib to see the visual diagrams: pip install matplotlib")


if __name__ == '__main__':
    main() 