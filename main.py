import streamlit as st

def main():
    # 페이지 기본 설정
    st.set_page_config(
        page_title="베스킨라빈스 키오스크 🍨",
        page_icon="🍦",
    )

    st.title("🍨 베스킨라빈스 키오스크 데모")
    st.write("어서 오세요! 달콤한 아이스크림 고르러 가볼까요? 😊")

    st.markdown("---")

    # 1. 매장/포장 선택
    st.subheader("1. 이용 방법 선택 🍽️ / 🛍️")
    eat_type = st.radio(
        "매장에서 드시나요, 포장해서 가져가시나요?",
        ["매장에서 먹고 갈게요 🍽️", "포장해서 가져갈게요 🛍️"],
        index=0,
    )

    st.markdown("---")

    # 2. 용기 선택
    st.subheader("2. 용기 선택 🧺")

    containers = {
        "싱글 레귤러 컵 (1스쿱)": {"max_scoops": 1, "price": 3500},
        "더블 주니어 컵 (2스쿱)": {"max_scoops": 2, "price": 5200},
        "파인트 (3스쿱)": {"max_scoops": 3, "price": 9500},
        "쿼터 (4스쿱)": {"max_scoops": 4, "price": 15500},
        "패밀리 (5스쿱)": {"max_scoops": 5, "price": 22000},
        "하프갤런 (6스쿱)": {"max_scoops": 6, "price": 26500},
    }

    container_names = list(containers.keys())
    container_choice = st.selectbox(
        "용기를 선택해 주세요 😊",
        ["-- 용기를 선택해 주세요 --"] + container_names,
    )

    if container_choice != "-- 용기를 선택해 주세요 --":
        max_scoops = containers[container_choice]["max_scoops"]
        price = containers[container_choice]["price"]

        st.info(
            f"👉 **{container_choice}** 는 최대 **{max_scoops}스쿱 이하**까지 선택할 수 있고, "
            f"가격은 **{price:,}원** 입니다. "
            "원하시는 만큼만 담으셔도 괜찮아요! 🍦"
        )

        st.markdown("---")

        # 3. 아이스크림 맛 선택
        st.subheader("3. 아이스크림 맛 선택 🍨")

        flavors = [
            "슈팅스타 🌠",
            "엄마는 외계인 👽",
            "민트초코 ♥️",
            "뉴욕 치즈케이크 🧀",
            "바람과 함께 사라지다 💨",
            "초콜릿 무스 🍫",
            "바닐라 클래식 🤍",
            "딸기 🍓",
            "녹차 🌿",
            "쿠키앤크림 🍪",
        ]

        flavor_options = ["선택 안 함"] + flavors

        # 스쿱별 선택 박스
        for i in range(1, max_scoops + 1):
            st.selectbox(
                f"{i}번 스쿱 아이스크림을 골라주세요 🍦",
                flavor_options,
                key=f"scoop_{i}",
            )

        # 실제로 선택된 맛들만 모으기 (선택 안 함 제외)
        selected_flavors = [
            st.session_state.get(f"scoop_{i}")
            for i in range(1, max_scoops + 1)
            if st.session_state.get(f"scoop_{i}") not in (None, "선택 안 함")
        ]

        st.markdown("---")

        # 4. 결제 방법 선택
        st.subheader("4. 결제 방법 선택 💳")
        payment_method = st.radio(
            "결제 방법을 선택해 주세요 😄",
            ["현금 결제 💵", "카드 결제 💳"],
            index=1,
        )

        st.markdown("---")

        # 주문 요약
        st.subheader("🧾 주문 내역 확인")

        st.write(f"**이용 방법:** {eat_type}")
        st.write(f"**용기:** {container_choice}")
        if selected_flavors:
            st.write("**선택한 맛:** " + ", ".join(selected_flavors))
        else:
            st.write("**선택한 맛:** 아직 선택하지 않으셨어요 ☁️")

        st.write(f"**최종 결제 금액:** 💰 **{price:,}원**")
