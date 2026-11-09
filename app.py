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
