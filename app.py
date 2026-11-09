
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal
import streamlit.components.v1 as components

# ============================================================
# SIGNAL LAB PRO — PROFESSIONAL SIGNAL PROCESSING LAB
# ============================================================

st.set_page_config(
    page_title="SIGNAL LAB PRO",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: linear-gradient(145deg,#080d1c,#101b31 65%,#0b1425);
    color: #edf4ff;
}
section[data-testid="stSidebar"] {
    background: #101a2d;
    border-right: 1px solid #263956;
}
.hero {
    padding: 24px;
    border: 1px solid #244a73;
    border-radius: 18px;
    background: linear-gradient(115deg,#112b4b,#10192d);
    margin-bottom: 18px;
}
.hero h1 {
    font-size: 38px;
    font-weight: 800;
    margin: 0;
    color: #ffffff;
}
.hero p {
    color: #a9c6e9;
    margin-bottom: 0;
}
.metric {
    padding: 15px;
    border-radius: 12px;
    background: #14233a;
    border: 1px solid #294260;
}
.metric-label {color:#91aaca;font-size:12px;}
.metric-value {color:#ffffff;font-size:24px;font-weight:700;}
.panel {
    background: #14233a;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #294260;
}
h2,h3 {color:#e9f3ff;}
div[data-testid="stMetric"] {
    background:#14233a;
    border:1px solid #294260;
    padding:12px;
    border-radius:12px;
}
.stButton button {
    border-radius:9px;
}
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------- ANIMATED HEADER --------------------

components.html("""
<div style="height:135px;overflow:hidden;border-radius:16px;
background:linear-gradient(110deg,#071426,#102e50);
position:relative;border:1px solid #28517c;">
<canvas id="wave" style="width:100%;height:135px;"></canvas>
<div style="position:absolute;top:17px;left:22px;pointer-events:none;">
<div style="font-size:28px;font-weight:800;color:white;">
⚡ SIGNAL LAB PRO
</div>
<div style="color:#a8c9ed;font-size:12px;letter-spacing:2px;">
ENGINEERING SIGNAL PROCESSING STUDIO
</div>
</div>
</div>
<script>
const c=document.getElementById("wave");
const ctx=c.getContext("2d");
function resize(){
 c.width=c.clientWidth*devicePixelRatio;
 c.height=c.clientHeight*devicePixelRatio;
 ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);
}
resize();
window.addEventListener("resize",resize);
let t=0;
function draw(){
 const w=c.clientWidth,h=c.clientHeight;
 ctx.clearRect(0,0,w,h);
 for(let k=0;k<4;k++){
  ctx.beginPath();
  for(let x=0;x<w;x+=2){
   let y=h*.65+Math.sin(x*.018+t+k)*12+
   Math.sin(x*.008-t*.7+k)*9+k*3;
   if(x===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
  }
  ctx.strokeStyle=["#39bfff","#a77cff","#4de0c2","#4d8fff"][k];
  ctx.globalAlpha=.75;
  ctx.lineWidth=1.8;
  ctx.stroke();
 }
 ctx.globalAlpha=1;
 t+=.045;
 requestAnimationFrame(draw);
}
draw();
</script>
""", height=145)

st.markdown("""
<div class="hero">
<h1>Signal Processing Laboratory</h1>
<p>Explore, generate, visualize and analyze signals in time and frequency domains.</p>
</div>
""", unsafe_allow_html=True)

# -------------------- FUNCTIONS --------------------

def make_signal(kind, t, amplitude, frequency, phase, fs, duty=0.5):
    w = 2 * np.pi * frequency * t + np.deg2rad(phase)

    if kind == "Sine":
        return amplitude * np.sin(w)
    if kind == "Cosine":
        return amplitude * np.cos(w)
    if kind == "Square":
        return amplitude * signal.square(w, duty=duty)
    if kind == "Triangle":
        return amplitude * signal.sawtooth(w, width=0.5)
    if kind == "Sawtooth":
        return amplitude * signal.sawtooth(w)
    if kind == "Impulse":
        x = np.zeros(len(t))
        x[len(t)//2] = amplitude
        return x
    if kind == "Step":
        return amplitude * (t >= 0).astype(float)
    if kind == "Rectified sine":
        return amplitude * np.abs(np.sin(w))
    if kind == "Damped sine":
        return amplitude * np.exp(-2*np.maximum(t,0)) * np.sin(w)
    if kind == "Chirp":
        return amplitude * signal.chirp(
            t, f0=max(frequency, 0.01),
            f1=max(frequency*4, 0.02),
            t1=max(t[-1], 0.01)
        )
    if kind == "Noise":
        rng = np.random.default_rng(42)
        return amplitude * rng.normal(0, 1, len(t))
    return amplitude * np.sin(w)


def spectrum(x, fs, mode, window_name, nfft):
    n = len(x)

    windows = {
        "Rectangular": np.ones(n),
        "Hann": np.hanning(n),
        "Hamming": np.hamming(n),
        "Blackman": np.blackman(n)
    }

    win = windows[window_name]
    xw = x * win

    if mode == "DTFT (Discrete-Time)":
        X = np.fft.fftshift(np.fft.fft(xw, n=nfft))
        f = np.fft.fftshift(np.fft.fftfreq(nfft, d=1))
        scale = np.sum(win)
        unit = "cycles/sample"
    else:
        X = np.fft.fftshift(np.fft.fft(xw, n=nfft)) / fs
        f = np.fft.fftshift(np.fft.fftfreq(nfft, d=1/fs))
        scale = np.sum(win) / fs
        unit = "Hz"

    magnitude = np.abs(X) / max(scale, 1e-12)
    phase = np.angle(X, deg=True)

    return f, magnitude, phase, X, unit


def create_plot(x, y, title, xlabel, ylabel, name, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines",
        name=name,
        line=dict(color=color, width=2.3)
    ))
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark",
        height=400,
        margin=dict(l=35,r=25,t=55,b=45),
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(12,25,43,0.8)"
    )
    fig.update_xaxes(showgrid=True, gridcolor="#263b55")
    fig.update_yaxes(showgrid=True, gridcolor="#263b55")
    return fig


def metric(label, value):
    st.markdown(
        f'<div class="metric"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True
    )


# -------------------- SIDEBAR --------------------

st.sidebar.title("⚙️ Laboratory Controls")

mode = st.sidebar.selectbox(
    "Transform mode",
    ["DTFT (Discrete-Time)", "CTFT (Continuous-Time)"]
)

st.sidebar.divider()
st.sidebar.subheader("Sampling configuration")

fs = st.sidebar.slider("Sampling frequency (Hz)", 10, 2000, 200)
N = st.sidebar.select_slider(
    "Number of samples",
    options=[32,64,128,256,512,1024,2048],
    value=256
)

duration = N / fs
t = np.arange(N) / fs
nfft = st.sidebar.selectbox(
    "FFT resolution",
    [512,1024,2048,4096,8192],
    index=2
)

st.sidebar.divider()
st.sidebar.subheader("Spectrum settings")
window_name = st.sidebar.selectbox(
    "Window function",
    ["Rectangular","Hann","Hamming","Blackman"]
)

st.sidebar.caption(
    "DTFT frequency is displayed in cycles/sample. "
    "CTFT is approximated numerically using the sampled finite record."
)

st.sidebar.divider()
st.sidebar.caption("SIGNAL LAB PRO | ECE Engineering Edition")

# -------------------- SIGNAL GENERATORS --------------------

st.header("01 · Signal Generator")

signal_types = [
    "Sine","Cosine","Square","Triangle","Sawtooth",
    "Impulse","Step","Rectified sine","Damped sine",
    "Chirp","Noise"
]

colA, colB = st.columns(2)

with colA:
    st.subheader("🔵 Signal A")
    kindA = st.selectbox("Signal A waveform", signal_types, index=0)
    ampA = st.number_input("Amplitude A", 0.0, 100.0, 1.0, 0.1)
    freqA = st.number_input("Frequency A (Hz)", 0.1, 1000.0, 5.0, 0.5)
    phaseA = st.slider("Phase A (degrees)", -180, 180, 0)
    dutyA = st.slider("Duty cycle A (%)", 5, 95, 50) / 100

with colB:
    st.subheader("🟠 Signal B")
    kindB = st.selectbox("Signal B waveform", signal_types, index=1)
    ampB = st.number_input("Amplitude B", 0.0, 100.0, 2.0, 0.1)
    freqB = st.number_input("Frequency B (Hz)", 0.1, 1000.0, 10.0, 0.5)
    phaseB = st.slider("Phase B (degrees)", -180, 180, 45)
    dutyB = st.slider("Duty cycle B (%)", 5, 95, 50) / 100

xA = make_signal(kindA,t,ampA,freqA,phaseA,fs,dutyA)
xB = make_signal(kindB,t,ampB,freqB,phaseB,fs,dutyB)
xSum = xA + xB

# -------------------- TIME DOMAIN --------------------

st.divider()
st.header("02 · Time-Domain Analysis")

time_tab1, time_tab2, time_tab3 = st.tabs([
    "Signal A & B","Combined signal","Signal statistics"
])

with time_tab1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t,y=xA,name="Signal A",
        line=dict(color="#39bfff",width=2.4)
    ))
    fig.add_trace(go.Scatter(
        x=t,y=xB,name="Signal B",
        line=dict(color="#ff965c",width=2.4)
    ))
    fig.update_layout(
        title="Signal Waveforms",
        xaxis_title="Time (seconds)",
        yaxis_title="Amplitude",
        template="plotly_dark",
        height=470,
        hovermode="x unified"
    )
    st.plotly_chart(fig,use_container_width=True)

with time_tab2:
    fig=create_plot(
        t,xSum,"Combined Signal",
        "Time (seconds)","Amplitude","A + B","#52e0bb"
    )
    st.plotly_chart(fig,use_container_width=True)

with time_tab3:
    stats = pd.DataFrame({
        "Parameter":["Mean","RMS","Peak","Minimum","Maximum","Standard deviation","Energy (sample sum)"],
        "Signal A":[
            np.mean(xA),np.sqrt(np.mean(xA**2)),
            np.max(np.abs(xA)),np.min(xA),np.max(xA),
            np.std(xA),np.sum(xA**2)
        ],
        "Signal B":[
            np.mean(xB),np.sqrt(np.mean(xB**2)),
            np.max(np.abs(xB)),np.min(xB),np.max(xB),
            np.std(xB),np.sum(xB**2)
        ]
    })
    st.dataframe(stats,use_container_width=True,hide_index=True)

# -------------------- FREQUENCY ANALYSIS --------------------

st.divider()
st.header("03 · Frequency-Domain Analysis")

fA,magA,phA,fftA,unit = spectrum(xA,fs,mode,window_name,nfft)
fB,magB,phB,fftB,_ = spectrum(xB,fs,mode,window_name,nfft)

freq_tab1,freq_tab2,freq_tab3,freq_tab4 = st.tabs([
    "Magnitude spectrum","Phase spectrum",
    "A vs B comparison","Complex spectrum"
])

with freq_tab1:
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=fA,y=magA,name="Signal A",line=dict(color="#39bfff")))
    fig.add_trace(go.Scatter(x=fB,y=magB,name="Signal B",line=dict(color="#ff965c")))
    fig.update_layout(
        title="Magnitude Spectrum",
        xaxis_title=f"Frequency ({unit})",
        yaxis_title="Normalized magnitude",
        template="plotly_dark",height=460,
        hovermode="x unified"
    )
    st.plotly_chart(fig,use_container_width=True)

with freq_tab2:
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=fA,y=phA,name="Signal A",line=dict(color="#39bfff")))
    fig.add_trace(go.Scatter(x=fB,y=phB,name="Signal B",line=dict(color="#ff965c")))
    fig.update_layout(
        title="Phase Spectrum",
        xaxis_title=f"Frequency ({unit})",
        yaxis_title="Phase (degrees)",
        template="plotly_dark",height=460,
        hovermode="x unified"
    )
    st.plotly_chart(fig,use_container_width=True)

with freq_tab3:
    st.subheader("Signal comparison")
    difference = xA-xB
    c1,c2,c3 = st.columns(3)
    c1.metric("Correlation",f"{np.corrcoef(xA,xB)[0,1]:.4f}" if np.std(xA)*np.std(xB)>0 else "Undefined")
    c2.metric("Mean squared error",f"{np.mean(difference**2):.5f}")
    c3.metric("Combined peak",f"{np.max(np.abs(xSum)):.4f}")

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=fA,y=magA,name="A"))
    fig.add_trace(go.Scatter(x=fB,y=magB,name="B"))
    fig.update_layout(
        title="Frequency Comparison",
        xaxis_title=unit,yaxis_title="Magnitude",
        template="plotly_dark",height=430
    )
    st.plotly_chart(fig,use_container_width=True)

with freq_tab4:
    fig=make_subplots(rows=2,cols=1,subplot_titles=("Real part","Imaginary part"))
    fig.add_trace(go.Scatter(x=fA,y=np.real(fftA),name="A real"),row=1,col=1)
    fig.add_trace(go.Scatter(x=fA,y=np.imag(fftA),name="A imaginary"),row=2,col=1)
    fig.update_layout(template="plotly_dark",height=550)
    st.plotly_chart(fig,use_container_width=True)

# -------------------- SPECTROGRAM --------------------

st.divider()
st.header("04 · Spectrogram & Time-Frequency Analysis")

spec_signal = st.selectbox(
    "Choose signal for spectrogram",
    ["Signal A","Signal B","Combined signal"]
)
selected = {"Signal A":xA,"Signal B":xB,"Combined signal":xSum}[spec_signal]

nperseg=min(128,N)
noverlap=min(nperseg-1,nperseg//2)

sf,stimes,Sxx=signal.spectrogram(
    selected,fs=fs,nperseg=nperseg,
    noverlap=noverlap
)

fig=go.Figure(data=go.Heatmap(
    x=stimes,y=sf,z=10*np.log10(Sxx+1e-12),
    colorscale="Turbo",
    colorbar=dict(title="Power (dB)")
))
fig.update_layout(
    title=f"Spectrogram — {spec_signal}",
    xaxis_title="Time (seconds)",
    yaxis_title="Frequency (Hz)",
    template="plotly_dark",height=470
)
st.plotly_chart(fig,use_container_width=True)

# -------------------- FILTER LAB --------------------

st.divider()
st.header("05 · Digital Filter Laboratory")

filter_col1,filter_col2 = st.columns(2)

with filter_col1:
    filter_type=st.selectbox(
        "Filter type",
        ["Low-pass","High-pass","Band-pass","Band-stop"]
    )
    order=st.slider("Filter order",1,10,4)

with filter_col2:
    cutoff1=st.number_input(
        "Cutoff frequency 1 (Hz)",
        min_value=0.1,max_value=float(fs/2-0.1),
        value=float(min(15,fs/4))
    )
    cutoff2=st.number_input(
        "Cutoff frequency 2 (Hz)",
        min_value=0.2,max_value=float(fs/2-0.05),
        value=float(min(35,fs/2-0.1))
    )
    filter_input=st.selectbox(
        "Input signal",["Signal A","Signal B","Combined signal"]
    )

filter_data={"Signal A":xA,"Signal B":xB,"Combined signal":xSum}[filter_input]

try:
    if filter_type in ["Low-pass","High-pass"]:
        wn=cutoff1/(fs/2)
        btype="lowpass" if filter_type=="Low-pass" else "highpass"
        sos=signal.butter(order,wn,btype=btype,output="sos")
    else:
        low=min(cutoff1,cutoff2)
        high=max(cutoff1,cutoff2)
        sos=signal.butter(
            order,[low/(fs/2),high/(fs/2)],
            btype="bandpass" if filter_type=="Band-pass" else "bandstop",
            output="sos"
        )

    if len(filter_data)>3*2*(order+1):
        filtered=signal.sosfiltfilt(sos,filter_data)
    else:
        filtered=signal.sosfilt(sos,filter_data)

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=t,y=filter_data,name="Original"))
    fig.add_trace(go.Scatter(x=t,y=filtered,name="Filtered"))
    fig.update_layout(
        title="Digital Filter Response",
        xaxis_title="Time (seconds)",
        yaxis_title="Amplitude",
        template="plotly_dark",height=430
    )
    st.plotly_chart(fig,use_container_width=True)

    st.download_button(
        "⬇️ Download filtered signal CSV",
        pd.DataFrame({"Time":t,"Original":filter_data,"Filtered":filtered}).to_csv(index=False),
        file_name="filtered_signal.csv",
        mime="text/csv"
    )
except Exception as e:
    st.error(f"Filter error: {e}")

# -------------------- CONVOLUTION --------------------

st.divider()
st.header("06 · Convolution & Correlation")

conv_col1,conv_col2=st.columns(2)

with conv_col1:
    conv_mode=st.selectbox(
        "Operation",["Convolution","Cross-correlation","Auto-correlation"]
    )
with conv_col2:
    conv_norm=st.checkbox("Normalize result",value=False)

if conv_mode=="Convolution":
    result=np.convolve(xA,xB,mode="full")
    lag=np.arange(len(result))
elif conv_mode=="Cross-correlation":
    result=signal.correlate(xA,xB,mode="full")
    lag=signal.correlation_lags(len(xA),len(xB),mode="full")
else:
    result=signal.correlate(xA,xA,mode="full")
    lag=signal.correlation_lags(len(xA),len(xA),mode="full")

if conv_norm and np.max(np.abs(result))>0:
    result=result/np.max(np.abs(result))

fig=create_plot(
    lag,result,conv_mode,
    "Sample lag","Amplitude","Result","#a77cff"
)
st.plotly_chart(fig,use_container_width=True)

# -------------------- 3D VISUALIZATION --------------------

st.divider()
st.header("07 · Three-Dimensional Signal Visualization")

fgrid=np.linspace(-fs/2,fs/2,nfft)
fig=go.Figure(data=[go.Surface(
    x=fgrid,y=[0,1],z=np.array([magA,magB]),
    colorscale="Viridis"
)])
fig.update_layout(
    title="3D Magnitude Spectrum Comparison",
    scene=dict(
        xaxis_title="Frequency (Hz)",
        yaxis_title="Signal",
        zaxis_title="Magnitude"
    ),
    template="plotly_dark",height=550
)
st.plotly_chart(fig,use_container_width=True)

# -------------------- EXPORT --------------------

st.divider()
st.header("08 · Export Laboratory Data")

export_df=pd.DataFrame({
    "Time_seconds":t,
    "Signal_A":xA,
    "Signal_B":xB,
    "Combined":xSum
})

st.download_button(
    "⬇️ Download all signals (CSV)",
    export_df.to_csv(index=False),
    file_name="signal_lab_data.csv",
    mime="text/csv",
    use_container_width=True
)

spectrum_df=pd.DataFrame({
    "Frequency":fA,
    "Magnitude_A":magA,
    "Phase_A_degrees":phA,
    "Magnitude_B":magB,
    "Phase_B_degrees":phB
})

st.download_button(
    "⬇️ Download spectrum data (CSV)",
    spectrum_df.to_csv(index=False),
    file_name="spectrum_analysis.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()

st.markdown("""
<div style="text-align:center;padding:22px;color:#8ca7c8;">
<b>⚡ SIGNAL LAB PRO</b><br>
Digital Signal Processing · Fourier Analysis · ECE Laboratory<br>
Built with Python, NumPy, SciPy, Streamlit and Plotly
</div>
""",unsafe_allow_html=True)
