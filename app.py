import io
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
from scipy import signal as sp_signal

# ============================================================
# SIGNAL LAB PRO | PROFESSIONAL SIGNAL PROCESSING WORKSTATION
# ============================================================

st.set_page_config(
    page_title="SIGNAL LAB PRO",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------- DESIGN ----------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@500;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #f8f7ff 0%, #eef2ff 55%, #f4f8ff 100%);
    color: #20243a;
    font-family: 'Inter', sans-serif;
}
section[data-testid="stSidebar"] {
    background: #f0efff;
    border-right: 1px solid #d8d5f2;
}
h1, h2, h3 {
    color: #28234f !important;
}
.stApp p, .stApp label, .stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stWidgetLabel"], .stApp .stCaption,
section[data-testid="stSidebar"] {
    color: #30334a;
}
.stApp input, .stApp textarea,
.stApp [data-baseweb="select"] > div {
    background-color: #ffffff;
    color: #20243a;
}
.hero {
    background: linear-gradient(120deg, #eeebff, #e6f3ff, #f3eaff);
    border: 1px solid #c9c2f0;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 8px 35px #4b43801c;
}
.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(27px, 4vw, 43px);
    font-weight: 800;
    letter-spacing: 3px;
    color: #5540b8;
}
.hero-sub {
    color: #555879;
    font-size: 14px;
    letter-spacing: 2px;
}
.metric-card {
    background: linear-gradient(135deg, #ffffff, #f1efff);
    border: 1px solid #d8d2f4;
    padding: 17px;
    border-radius: 13px;
    min-height: 90px;
}
.metric-label {
    color: #62647d;
    font-size: 12px;
    text-transform: uppercase;
}
.metric-value {
    color: #5140b5;
    font-size: 25px;
    font-weight: 800;
}
.stButton button {
    border-radius: 9px;
    border: 1px solid #6654c7;
    background: linear-gradient(120deg, #6654c7, #8069d8);
    color: white;
    font-weight: 700;
}
.stButton button:hover {
    border-color: #44339e;
    color: #ffffff;
}
div[data-testid="stTabs"] button {
    color: #454064;
    font-weight: 700;
}
hr {
    border-color: #d8d5e8;
}
</style>
""", unsafe_allow_html=True)


# --------------------- ANIMATED WAVES ------------------------

components.html("""
<div style="height:145px;position:relative;overflow:hidden;
background:linear-gradient(120deg,#eeeaff,#e5f3ff,#f4eaff);
border:1px solid #c9c2f0;border-radius:16px;">
<div style="position:absolute;top:12px;left:20px;color:#5540b8;
font-family:Arial;font-size:12px;letter-spacing:3px;">
LIVE SIGNAL ENVIRONMENT
</div>
<svg viewBox="0 0 1200 130" preserveAspectRatio="none"
style="width:100%;height:100%;position:absolute;top:15px;">
<defs>
<linearGradient id="wave1"><stop stop-color="#168bd2"/>
<stop offset="1" stop-color="#6654c7"/></linearGradient>
<linearGradient id="wave2"><stop stop-color="#8b5cf6"/>
<stop offset="1" stop-color="#d9468f"/></linearGradient>
</defs>
<path d="M0 65 Q75 5 150 65 T300 65 T450 65 T600 65 T750 65 T900 65 T1050 65 T1200 65"
fill="none" stroke="url(#wave1)" stroke-width="3">
<animateTransform attributeName="transform" type="translate"
from="0 0" to="-300 0" dur="3s" repeatCount="indefinite"/>
</path>
<path d="M0 75 Q75 125 150 75 T300 75 T450 75 T600 75 T750 75 T900 75 T1050 75 T1200 75"
fill="none" stroke="url(#wave2)" stroke-width="2.5" opacity=".9">
<animateTransform attributeName="transform" type="translate"
from="-300 0" to="0 0" dur="4s" repeatCount="indefinite"/>
</path>
<path d="M0 68 Q35 20 70 68 T140 68 T210 68 T280 68 T350 68 T420 68 T490 68 T560 68 T630 68 T700 68 T770 68 T840 68 T910 68 T980 68 T1050 68 T1120 68 T1190 68"
fill="none" stroke="#ffffff" stroke-width="1" opacity=".35">
<animateTransform attributeName="transform" type="translate"
from="0 0" to="-280 0" dur="2s" repeatCount="indefinite"/>
</path>
</svg>
</div>
""", height=155)


# ------------------------- HEADER ----------------------------

st.markdown("""
<div class="hero">
<div class="hero-title">SIGNAL LAB PRO</div>
<div style="font-size:17px;color:#30334a;font-weight:600;">
ADVANCED SIGNAL PROCESSING WORKSTATION
</div>
<div class="hero-sub">
DTFT · CTFT · FFT · SPECTRAL ANALYSIS · SIGNAL RECONSTRUCTION
</div>
</div>
""", unsafe_allow_html=True)


# ----------------------- FUNCTIONS --------------------------

def generate_signal(kind, t, amplitude, frequency, phase_deg, fs):
    phase = np.deg2rad(phase_deg)
    angle = 2 * np.pi * frequency * t + phase

    if kind == "Sine":
        return amplitude * np.sin(angle)
    elif kind == "Cosine":
        return amplitude * np.cos(angle)
    elif kind == "Square":
        return amplitude * sp_signal.square(angle)
    elif kind == "Triangle":
        return amplitude * sp_signal.sawtooth(angle, width=0.5)
    elif kind == "Sawtooth":
        return amplitude * sp_signal.sawtooth(angle)
    elif kind == "Pulse":
        return amplitude * (np.abs((t * frequency) % 1) < 0.25).astype(float)
    elif kind == "Damped Sine":
        return amplitude * np.exp(-2 * np.maximum(t, 0)) * np.sin(angle)
    elif kind == "Exponential":
        return amplitude * np.exp(-2 * np.maximum(t, 0))
    elif kind == "Chirp":
        return amplitude * sp_signal.chirp(
            t, f0=max(0.1, frequency / 4),
            t1=max(t[-1], 0.001),
            f1=frequency * 2
        )
    elif kind == "Impulse":
        x = np.zeros(len(t))
        x[len(t) // 2] = amplitude
        return x
    elif kind == "Step":
        return amplitude * (t >= 0).astype(float)

    return amplitude * np.sin(angle)


def apply_window(x, window_name):
    if window_name == "Rectangular":
        return x.copy()
    if window_name == "Hann":
        return x * np.hanning(len(x))
    if window_name == "Hamming":
        return x * np.hamming(len(x))
    if window_name == "Blackman":
        return x * np.blackman(len(x))
    if window_name == "Bartlett":
        return x * np.bartlett(len(x))
    return x.copy()


def calculate_transform(x, fs, mode, window_name, nfft, freq_limit):
    xw = apply_window(x, window_name)

    if mode == "DTFT":
        # Numerical DTFT evaluated directly on a frequency grid.
        omega = np.linspace(-np.pi, np.pi, nfft, endpoint=False)
        n = np.arange(len(xw))
        X = np.exp(-1j * np.outer(omega, n)) @ xw
        f = omega / (2 * np.pi)
        unit = "cycles/sample"
    else:
        # Numerical CTFT approximation using a zero-padded FFT.
        dt = 1 / fs
        X = np.fft.fftshift(np.fft.fft(xw, n=nfft)) * dt
        f = np.fft.fftshift(np.fft.fftfreq(nfft, d=dt))
        unit = "Hz"

    keep = np.abs(f) <= freq_limit
    return f[keep], X[keep], unit, xw


def make_spectrum(f, X, display_mode):
    mag = np.abs(X)

    if display_mode == "Normalized":
        mag = mag / (np.max(mag) + 1e-12)
    elif display_mode == "Decibels (dB)":
        mag = 20 * np.log10(mag / (np.max(mag) + 1e-12) + 1e-12)

    return mag


def dominant_frequency(f, X):
    if len(f) < 2:
        return 0.0
    idx = np.argmax(np.abs(X))
    return float(f[idx])


def chart_layout(fig, height=430, title=None):
    fig.update_layout(
        title=title,
        height=height,
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#fbfaff",
        font=dict(color="#30334a", family="Arial"),
        margin=dict(l=35, r=25, t=55, b=45),
        hovermode="x unified",
        legend=dict(orientation="h", y=1.12),
        xaxis=dict(showgrid=True, gridcolor="#e2e0ed",
                   zerolinecolor="#b9b4d0"),
        yaxis=dict(showgrid=True, gridcolor="#e2e0ed",
                   zerolinecolor="#b9b4d0")
    )
    return fig


def metric(label, value):
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True
    )


# ---------------------- CONTROL PANEL -----------------------

st.sidebar.title("⚙️ CONTROL CENTER")
st.sidebar.caption("Configure your signal laboratory")

mode = st.sidebar.selectbox(
    "Transform Mode",
    ["DTFT", "CTFT"]
)

signal_types = [
    "Sine", "Cosine", "Square", "Triangle",
    "Sawtooth", "Pulse", "Damped Sine",
    "Exponential", "Chirp", "Impulse", "Step"
]

signal_type = st.sidebar.selectbox(
    "Signal Waveform",
    signal_types
)

fs = st.sidebar.slider(
    "Sampling Frequency (Hz)", 10, 2000, 100
)

N = st.sidebar.slider(
    "Number of Samples", 32, 2048, 256, step=32
)

duration = N / fs
t = np.arange(N) / fs

st.sidebar.divider()
st.sidebar.subheader("📊 Spectrum Settings")

window_name = st.sidebar.selectbox(
    "Window Function",
    ["Rectangular", "Hann", "Hamming",
     "Blackman", "Bartlett"]
)

nfft = st.sidebar.select_slider(
    "FFT / Transform Resolution",
    options=[256, 512, 1024, 2048, 4096],
    value=2048
)

display_mode = st.sidebar.selectbox(
    "Magnitude Scale",
    ["Linear", "Normalized", "Decibels (dB)"]
)

if mode == "DTFT":
    freq_limit = st.sidebar.slider(
        "Frequency range (cycles/sample)",
        0.05, 0.5, 0.5, step=0.05
    )
else:
    freq_limit = st.sidebar.slider(
        "Frequency range (Hz)",
        1, max(1, fs // 2), max(1, fs // 2)
    )

st.sidebar.divider()
st.sidebar.subheader("🔬 Signal A")

a_amp = st.sidebar.number_input(
    "A Amplitude", 0.0, 100.0, 1.0, 0.1
)
a_freq = st.sidebar.number_input(
    "A Frequency (Hz)", 0.1, 10000.0, 5.0, 0.5
)
a_phase = st.sidebar.slider(
    "A Phase (degrees)", -360, 360, 0
)

st.sidebar.divider()
st.sidebar.subheader("🔬 Signal B")

enable_b = st.sidebar.toggle("Enable Signal B", True)

b_amp = st.sidebar.number_input(
    "B Amplitude", 0.0, 100.0, 2.0, 0.1,
    disabled=not enable_b
)
b_freq = st.sidebar.number_input(
    "B Frequency (Hz)", 0.1, 10000.0, 10.0, 0.5,
    disabled=not enable_b
)
b_phase = st.sidebar.slider(
    "B Phase (degrees)", -360, 360, 45,
    disabled=not enable_b
)

# ---------------------- SIGNAL CREATION ---------------------

xA = generate_signal(
    signal_type, t, a_amp, a_freq, a_phase, fs
)

xB = generate_signal(
    signal_type, t, b_amp, b_freq, b_phase, fs
) if enable_b else np.zeros(N)

xTotal = xA + xB

# ---------------------- TRANSFORM ---------------------------

fA, XA, unit, xAw = calculate_transform(
    xA, fs, mode, window_name, nfft, freq_limit
)

fB, XB, _, xBw = calculate_transform(
    xB, fs, mode, window_name, nfft, freq_limit
)

fT, XT, _, xTw = calculate_transform(
    xTotal, fs, mode, window_name, nfft, freq_limit
)

magA = make_spectrum(fA, XA, display_mode)
magB = make_spectrum(fB, XB, display_mode)
magT = make_spectrum(fT, XT, display_mode)

phaseA = np.angle(XA, deg=True)
phaseB = np.angle(XB, deg=True)
phaseT = np.angle(XT, deg=True)

# ----------------------- MAIN METRICS ------------------------

st.subheader("📡 System Overview")

m1, m2, m3, m4 = st.columns(4)

with m1:
    metric("Transform", mode)
with m2:
    metric("Sample Count", str(N))
with m3:
    metric("Sampling Rate", f"{fs} Hz")
with m4:
    metric("Frequency Resolution", f"{fs / nfft:.4g} Hz")

st.caption(
    "DTFT frequency is expressed in cycles/sample. "
    "CTFT frequency is expressed in Hz. "
    "CTFT is numerically approximated from sampled data."
)

# -------------------------- TABS -----------------------------

tabs = st.tabs([
    "🌊 Time Domain",
    "📈 Magnitude Spectrum",
    "📐 Phase Spectrum",
    "⚖️ Comparison",
    "🧮 Signal Analysis",
    "💾 Export Data"
])
# ======================== TIME DOMAIN =======================

with tabs[0]:
    st.subheader("Time-Domain Signal Visualization")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=xA,
        name="Signal A",
        mode="lines+markers" if N <= 128 else "lines",
        line=dict(color="#168bd2", width=2.5),
        marker=dict(size=5)
    ))

    if enable_b:
        fig.add_trace(go.Scatter(
            x=t, y=xB,
            name="Signal B",
            mode="lines",
            line=dict(color="#d9468f", width=2)
        ))

        fig.add_trace(go.Scatter(
            x=t, y=xTotal,
            name="Combined Signal",
            mode="lines",
            line=dict(color="#b7791f", width=2, dash="dot")
        ))

    fig.update_layout(
        xaxis_title="Time (seconds)",
        yaxis_title="Amplitude"
    )
    st.plotly_chart(chart_layout(fig, 450), use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Signal A Peak", f"{np.max(np.abs(xA)):.4f}")
        st.metric("Signal A RMS", f"{np.sqrt(np.mean(xA**2)):.4f}")

    with c2:
        st.metric("Signal B Peak", f"{np.max(np.abs(xB)):.4f}")
        st.metric("Combined RMS", f"{np.sqrt(np.mean(xTotal**2)):.4f}")


# ====================== MAGNITUDE SPECTRUM ==================

with tabs[1]:
    st.subheader("Frequency-Domain Magnitude Analysis")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=fA, y=magA,
        name="Signal A",
        line=dict(color="#168bd2", width=2)
    ))

    if enable_b:
        fig.add_trace(go.Scatter(
            x=fB, y=magB,
            name="Signal B",
            line=dict(color="#d9468f", width=2)
        ))

        fig.add_trace(go.Scatter(
            x=fT, y=magT,
            name="Combined",
            line=dict(color="#b7791f", width=1.8)
        ))

    fig.update_layout(
        title="Magnitude Spectrum",
        xaxis_title=f"Frequency ({unit})",
        yaxis_title=f"Magnitude ({display_mode})"
    )
    st.plotly_chart(chart_layout(fig, 500), use_container_width=True)

    st.info(
        "Tip: Zoom into the spectrum using your mouse. "
        "Hover over a peak to inspect its frequency and magnitude."
    )


# ======================== PHASE SPECTRUM =====================

with tabs[2]:
    st.subheader("Phase Spectrum Analysis")

    phase_display = st.selectbox(
        "Phase Representation",
        ["Wrapped Phase", "Unwrapped Phase"]
    )

    pA = np.unwrap(np.angle(XA)) * 180 / np.pi if phase_display == "Unwrapped Phase" else phaseA
    pB = np.unwrap(np.angle(XB)) * 180 / np.pi if phase_display == "Unwrapped Phase" else phaseB
    pT = np.unwrap(np.angle(XT)) * 180 / np.pi if phase_display == "Unwrapped Phase" else phaseT

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=fA, y=pA,
        name="Signal A",
        line=dict(color="#168bd2", width=2)
    ))

    if enable_b:
        fig.add_trace(go.Scatter(
            x=fB, y=pB,
            name="Signal B",
            line=dict(color="#d9468f", width=2)
        ))

        fig.add_trace(go.Scatter(
            x=fT, y=pT,
            name="Combined",
            line=dict(color="#b7791f", width=1.8)
        ))

    fig.update_layout(
        title="Phase Spectrum",
        xaxis_title=f"Frequency ({unit})",
        yaxis_title="Phase (degrees)"
    )
    st.plotly_chart(chart_layout(fig, 480), use_container_width=True)


# ========================= COMPARISON =======================

with tabs[3]:
    st.subheader("Signal A vs Signal B")

    if enable_b:
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=[
                "Time-Domain Comparison",
                "Magnitude Spectrum Comparison"
            ],
            vertical_spacing=0.15
        )

        fig.add_trace(go.Scatter(
            x=t, y=xA, name="Signal A",
            line=dict(color="#168bd2", width=2)
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=t, y=xB, name="Signal B",
            line=dict(color="#d9468f", width=2)
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=fA, y=magA, name="Spectrum A",
            line=dict(color="#168bd2", width=2)
        ), row=2, col=1)

        fig.add_trace(go.Scatter(
            x=fB, y=magB, name="Spectrum B",
            line=dict(color="#d9468f", width=2)
        ), row=2, col=1)

        fig.update_layout(height=750)
        fig.update_xaxes(title_text="Time (seconds)", row=1, col=1)
        fig.update_xaxes(title_text=f"Frequency ({unit})", row=2, col=1)

        st.plotly_chart(
            chart_layout(fig, 750),
            use_container_width=True
        )

        st.subheader("Signal Difference")

        difference = xA - xB

        diff_fig = go.Figure()
        diff_fig.add_trace(go.Scatter(
            x=t, y=difference,
            name="A - B",
            fill="tozeroy",
            line=dict(color="#b7791f", width=2)
        ))
        diff_fig.update_layout(
            xaxis_title="Time (seconds)",
            yaxis_title="Amplitude difference"
        )
        st.plotly_chart(
            chart_layout(diff_fig, 350),
            use_container_width=True
        )

        st.metric(
            "Difference RMS",
            f"{np.sqrt(np.mean(difference**2)):.5f}"
        )
    else:
        st.warning("Enable Signal B in the sidebar to compare two signals.")
            # ======================= SIGNAL ANALYSIS ====================

with tabs[4]:
    st.subheader("Advanced Signal Measurements")

    dominant_A = dominant_frequency(fA, XA)
    dominant_B = dominant_frequency(fB, XB) if enable_b else 0

    a1, a2, a3 = st.columns(3)

    with a1:
        st.metric("Signal A Dominant Frequency",
                  f"{dominant_A:.5g} {unit}")
    with a2:
        st.metric("Signal A Mean",
                  f"{np.mean(xA):.5f}")
    with a3:
        st.metric("Signal A Standard Deviation",
                  f"{np.std(xA):.5f}")

    st.divider()

    st.subheader("Spectral Peak Detection")

    peaks, properties = sp_signal.find_peaks(
        np.abs(XA),
        prominence=max(np.max(np.abs(XA)) * 0.02, 1e-10)
    )

    peak_data = pd.DataFrame({
        "Frequency": fA[peaks],
        "Magnitude": np.abs(XA[peaks]),
        "Phase (degrees)": phaseA[peaks]
    })

    if len(peak_data):
        peak_data = peak_data.sort_values(
            "Magnitude", ascending=False
        ).head(20)
        st.dataframe(
            peak_data.round(5),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.write("No significant spectral peaks detected.")

    st.divider()

    st.subheader("Signal Statistics")

    stats = pd.DataFrame({
        "Parameter": [
            "Maximum",
            "Minimum",
            "Mean",
            "RMS",
            "Variance",
            "Standard Deviation",
            "Energy (sample sum)",
            "Peak-to-Peak"
        ],
        "Signal A": [
            np.max(xA),
            np.min(xA),
            np.mean(xA),
            np.sqrt(np.mean(xA**2)),
            np.var(xA),
            np.std(xA),
            np.sum(xA**2),
            np.ptp(xA)
        ],
        "Signal B": [
            np.max(xB),
            np.min(xB),
            np.mean(xB),
            np.sqrt(np.mean(xB**2)),
            np.var(xB),
            np.std(xB),
            np.sum(xB**2),
            np.ptp(xB)
        ]
    })

    st.dataframe(
        stats.round(6),
        use_container_width=True,
        hide_index=True
    )


# ======================== DATA EXPORT =======================

with tabs[5]:
    st.subheader("Export Your Signal Data")

    export_df = pd.DataFrame({
        "Time_seconds": t,
        "Signal_A": xA,
        "Signal_B": xB,
        "Combined_Signal": xTotal
    })

    spectrum_df = pd.DataFrame({
        f"Frequency_{unit}": fA,
        "Magnitude_A": np.abs(XA),
        "Phase_A_degrees": phaseA,
        "Magnitude_B": np.abs(XB),
        "Phase_B_degrees": phaseB,
        "Magnitude_Combined": np.abs(XT),
        "Phase_Combined_degrees": phaseT
    })

    st.write("**Time-domain data preview**")
    st.dataframe(
        export_df.head(20),
        use_container_width=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.download_button(
            "⬇ Download Signal CSV",
            export_df.to_csv(index=False).encode("utf-8"),
            "signal_lab_data.csv",
            "text/csv",
            use_container_width=True
        )

    with c2:
        st.download_button(
            "⬇ Download Spectrum CSV",
            spectrum_df.to_csv(index=False).encode("utf-8"),
            "signal_lab_spectrum.csv",
            "text/csv",
            use_container_width=True
        )

    st.divider()

    st.subheader("Download Complete Analysis Report")

    report = io.BytesIO()

    with pd.ExcelWriter(report, engine="openpyxl") as writer:
        export_df.to_excel(
            writer, sheet_name="Time Domain", index=False
        )
        spectrum_df.to_excel(
            writer, sheet_name="Frequency Domain", index=False
        )
        stats.to_excel(
            writer, sheet_name="Statistics", index=False
        )

    st.download_button(
        "📊 Download Excel Analysis Report",
        report.getvalue(),
        "Signal_Lab_Pro_Report.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )


# ------------------------- FOOTER ---------------------------

st.divider()

st.markdown("""
<div style="text-align:center;padding:20px;color:#62647d;">
<div style="font-family:Orbitron;font-size:19px;color:#5540b8;">
SIGNAL LAB PRO
</div>
Professional Digital Signal Processing Workstation<br>
DTFT · CTFT · FFT · Frequency Analysis · Signal Processing<br><br>
<span style="font-size:11px;">
Built with Python · NumPy · SciPy · Streamlit · Plotly
</span>
</div>
""", unsafe_allow_html=True)
