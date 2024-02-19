import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def transmission_coefficient(E, V0, width):
    k1 = np.sqrt(2 * E)
    k2 = np.sqrt(2 * (E - V0))
    T = 4 * k1 * k2 / ((k1 + k2) ** 2) * np.exp(-2 * k1 * width)
    return T

def wave_function(x, E, V0, width):
    k1 = np.sqrt(2 * E)
    k2 = np.sqrt(2 * (E - V0))
    A = 1.0
    B = A * np.exp(-k1 * width)
    C = A * (k1 / k2) * np.exp(k1 * width)
    D = B - C
    wave_func = np.piecewise(x,
                             [x < 0, (x >= 0) & (x <= width), x > width],
                             [lambda x: A * np.exp(1j * k1 * x) + B * np.exp(-1j * k1 * x),
                              lambda x: C * np.exp(1j * k2 * x),
                              lambda x: D * np.exp(-1j * k1 * x)])
    return wave_func

def main():
    st.title('Step Potential Wave Function and Transmission Coefficient')

    # User input
    E = st.number_input('Enter energy of the particle (in eV)', min_value=0.1, max_value=100.0, value=1.0, step=0.1)
    V0 = st.number_input('Enter height of the potential step (in eV)', min_value=0.0, max_value=100.0, value=10.0, step=0.1)
    width = st.number_input('Enter width of the potential step barrier (in nm)', min_value=0.1, max_value=100.0, value=1.0, step=0.1)

    # Calculate transmission coefficient
    T = transmission_coefficient(E, V0, width)

    # Display result
    st.write(f'Transmission coefficient: {T:.4f}')

    # Plot transmission coefficient vs. energy
    energies = np.linspace(0.1, 100.0, 500)
    T_values = [transmission_coefficient(energy, V0, width) for energy in energies]

    plt.figure(figsize=(8, 6))
    plt.plot(energies, T_values)
    plt.xlabel('Energy (eV)')
    plt.ylabel('Transmission Coefficient')
    plt.title('Transmission Coefficient vs. Energy')
    st.pyplot(plt)

    # Plot wave function
    x = np.linspace(-2*width, 2*width, 1000)
    wave_func = wave_function(x, E, V0, width)

    plt.figure(figsize=(8, 6))
    plt.plot(x, wave_func.real, label='Real Part')
    plt.plot(x, wave_func.imag, label='Imaginary Part')
    plt.xlabel('Position (nm)')
    plt.ylabel('Wave Function')
    plt.title('Wave Function in Different Regions')
    plt.legend()
    st.pyplot(plt)

if __name__ == "__main__":
    main()
