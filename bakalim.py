import requests
import streamlit as st

wmo_turkce = {
    0: "Açık gökyüzü",
    1: "Genellikle açık",
    2: "Parçalı bulutlu",
    3: "Çok bulutlu / Kapalı",
    45: "Sisli",
    48: "Kırağılı sis",
    51: "Hafif çisenti",
    53: "Orta şiddette çisenti",
    55: "Yoğun çisenti",
    61: "Hafif yağmurlu",
    63: "Orta şiddette yağmurlu",
    65: "Şiddetli yağmurlu",
    71: "Hafif kar yağışlı",
    73: "Orta şiddette kar yağışlı",
    75: "Yoğun kar yağışlı",
    95: "Gök gürültülü fırtına",
}

def get_wmo_text(code):
    return wmo_turkce.get(code, "Bilinmeyen hava durumu")

st.set_page_config(page_title="Chicago Hava Durumu", page_icon="👽", layout="centered")


st.title("☀️Chicago Hava Durumu☀️")
st.header("Konum Bilgisi")
try:
    with st.spinner("Chicago ile ilgili bilgiler alınıyor..."):
        enlemveboylam = requests.get("https://geocoding-api.open-meteo.com/v1/search?name=Chicago&count=1&language=tr&format=json").json()
        ilk_sonuc = enlemveboylam["results"][0]
        ülkevesehir = ilk_sonuc["timezone"]
        enlem = ilk_sonuc["latitude"]
        boylam = ilk_sonuc["longitude"]
        nüfus = ilk_sonuc["population"]
        url = f"https://api.open-meteo.com/v1/forecast?latitude={enlem}&longitude={boylam}&current_weather=true&current_weather_units=true"
        hava_url = requests.get(url).json()
        sıcaklık = hava_url["current_weather"]["temperature"]
        s_isaret = hava_url["current_weather_units"]["temperature"]
        ruzgar = hava_url["current_weather"]["windspeed"]
        r_isaret = hava_url["current_weather_units"]["windspeed"]
        wmo = hava_url["current_weather"]["weathercode"]
    st.info(f"📍 {ülkevesehir}")
    st.header("Genel Bilgiler")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Sıcaklık", value=f"{sıcaklık}{s_isaret}")
    with col2:
        st.metric(label="Rüzgar Hızı", value=f"{ruzgar}{r_isaret}")
    with col3:
        st.metric(label="Nüfus", value=f"{nüfus} kişi")
    st.success(f"Hava Durumu: {get_wmo_text(wmo)}")
except Exception as e:
    st.error("Bir Hata Oluştu...")
    st.write("Hata Kodu: " + str(e))
if st.button("Yenile"):
    st.rerun()