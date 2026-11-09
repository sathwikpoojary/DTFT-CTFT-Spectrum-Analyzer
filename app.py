
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="DTFT / CTFT Analyzer",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Signal Spectrum Analyzer")
st.caption("Professional DTFT & CTFT analysis and comparison")

st.sidebar.header("Analysis Settings")

mode = st.sidebar.selectbox(
    "Transform mode",
    ["DTFT (Discrete-Time)", "CTFT (Continuous-Time)"]
)

signal_type = st.sidebar.selectbox(
    "Signal type",
    ["Sine", "Cosine"]
)

if mode.startswith("DTFT"):
    st.info("DTFT is evaluated numerically over the frequency range −π to π.")
else:
    st.info("CTFT is approximated numerically using sampled continuous-time signals and FFT.")

if mode.startswith("DTFT"):
    count = st.sidebar.slider("Number of samples", 16, 512, 128)
    n = np.arange(count)
    t = None
else:
    duration = st.sidebar.slider("Signal duration (seconds)", 1.0, 10.0, 2.0)
    fs = st.sidebar.select_slider(
        "Sampling frequency (Hz)",
        options=[100, 200, 500, 1000, 2000],
        value=500
    )
    t = np.arange(0, duration, 1/fs)
    n = None

st.sidebar.divider()
st.sidebar.write("Configure both signals below.")

col1, col2 = st.columns(2)

def signal_controls(label, default_amp, default_freq, default_phase):
    with st.container(border=True):
        st.subheader(label)
        amplitude = st.number_input(
            f"{label} amplitude",
            min_value=0.0, max_value=20.0,
            value=default_amp, step=0.5,
            key=f"{label}_amp"
        )
        frequency = st.number_input(
            f"{label} frequency (Hz)",
            min_value=0.1, max_value=100.0,
            value=default_freq, step=0.5,
            key=f"{label}_freq"
        )
        phase = st.slider(
            f"{label} phase (degrees)",
            -180, 180, default_phase,
            key=f"{label}_phase"
        )
    return amplitude, frequency, np.deg2rad(phase)

with col1:
    A1, f1, p1 = signal_controls("Signal A", 1.0, 5.0, 0)

with col2:
    A2, f2, p2 = signal_controls("Signal B", 2.0, 10.0, 45)

def generate_signal(A, f, phase):
    if mode.startswith("DTFT"):
        # Discrete-time sinusoid: x[n] = A sin(2πfn + phase)
        # Frequency is expressed in cycles/sample.
        x = A * (
            np.sin(2 * np.pi * f * n / 100 + phase)
            if signal_type == "Sine"
            else np.cos(2 * np.pi * f * n / 100 + phase)
        )
        return x

    if signal_type == "Sine":
        return A * np.sin(2 * np.pi * f * t + phase)
    return A * np.cos(2 * np.pi * f * t + phase)

x1 = generate_signal(A1, f1, p1)
x2 = generate_signal(A2, f2, p2)

def calculate_spectrum(x):
    if mode.startswith("DTFT"):
        omega = np.linspace(-np.pi, np.pi, 2048)
        indices = np.arange(len(x))
        X = np.exp(-1j * np.outer(omega, indices)) @ x
        frequency_axis = omega / (2 * np.pi)
        magnitude = np.abs(X)
        phase = np.angle(X)
        axis_label = "Normalized frequency (cycles/sample)"
    else:
        dt = 1 / fs
        X = np.fft.fftshift(np.fft.fft(x)) * dt
        frequency_axis = np.fft.fftshift(
            np.fft.fftfreq(len(x), d=dt)
        )
        magnitude = np.abs(X)
        phase = np.angle(X)
        axis_label = "Frequency (Hz)"

    return frequency_axis, magnitude, phase, axis_label

faxis, mag1, ph1, axis_label = calculate_spectrum(x1)
_, mag2, ph2, _ = calculate_spectrum(x2)

st.divider()
st.header("Time-Domain Signals")

fig, ax = plt.subplots(2, 1, figsize=(11, 6))

if mode.startswith("DTFT"):
    ax[0].stem(n, x1, linefmt="C0-", markerfmt="C0o", basefmt=" ")
    ax[1].stem(n, x2, linefmt="C1-", markerfmt="C1o", basefmt=" ")
    ax[0].set_xlabel("Sample index n")
    ax[1].set_xlabel("Sample index n")
else:
    ax[0].plot(t, x1)
    ax[1].plot(t, x2)
    ax[0].set_xlabel("Time (seconds)")
    ax[1].set_xlabel("Time (seconds)")

ax[0].set_title("Signal A")
ax[1].set_title("Signal B")

for a in ax:
    a.set_ylabel("Amplitude")
    a.grid(True)

st.pyplot(fig)
plt.close(fig)

st.divider()
st.header("Frequency-Domain Analysis")

tabs = st.tabs(["Magnitude Spectrum", "Phase Spectrum", "Comparison"])

with tabs[0]:
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(faxis, mag1, label="Signal A")
    ax.plot(faxis, mag2, label="Signal B")
    ax.set_title("Magnitude Spectrum")
    ax.set_xlabel(axis_label)
    ax.set_ylabel("Magnitude")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    plt.close(fig)

with tabs[1]:
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(faxis, np.unwrap(ph1), label="Signal A")
    ax.plot(faxis, np.unwrap(ph2), label="Signal B")
    ax.set_title("Phase Spectrum")
    ax.set_xlabel(axis_label)
    ax.set_ylabel("Phase (radians)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    plt.close(fig)

with tabs[2]:
    fig, ax = plt.subplots(2, 1, figsize=(11, 7))

    ax[0].plot(faxis, mag1, label="Signal A")
    ax[0].plot(faxis, mag2, label="Signal B")
    ax[0].set_title("Magnitude Comparison")
    ax[0].legend()
    ax[0].grid(True)

    ax[1].plot(faxis, np.unwrap(ph1), label="Signal A")
    ax[1].plot(faxis, np.unwrap(ph2), label="Signal B")
    ax[1].set_title("Phase Comparison")
    ax[1].set_xlabel(axis_label)
    ax[1].legend()
    ax[1].grid(True)

    st.pyplot(fig)
    plt.close(fig)

st.divider()
st.subheader("Signal Parameters")

c1, c2 = st.columns(2)
c1.metric("Signal A peak amplitude", f"{np.max(np.abs(x1)):.3f}")
c2.metric("Signal B peak amplitude", f"{np.max(np.abs(x2)):.3f}")

st.caption(
    "Educational numerical analyzer. CTFT uses finite-duration sampled "
    "signals; DTFT uses a finite-length sequence."
)
