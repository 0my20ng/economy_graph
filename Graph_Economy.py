import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from matplotlib.patches import Polygon

# 한글 폰트 설정 (Windows 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ✅ 소비자 잉여 계산 함수 (삼각형 넓이)
def consumer_surplus(a, b, p_eq, q_eq):
    return 0.5 * q_eq * ((a / b) - p_eq)

# ✅ 생산자 잉여 계산 함수 (삼각형 넓이)
def producer_surplus(c, d, p_eq, q_eq):
    return 0.5 * q_eq * (p_eq - (-c / d))

# ✅ 초과수요 및 초과공급 계산
def calculate_surplus_shortage(a, b, c, d, control_price):
    qd = a - b * control_price
    qs = c + d * control_price
    if qd > qs:
        return "초과 수요", qd - qs
    elif qs > qd:
        return "초과 공급", qs - qd
    else:
        return "균형", 0

# ✅ 시장 시뮬레이션 및 시각화 함수
def simulate_market(a, b, c, d, tax=0, subsidy=0, price_control_type=None, price_control=None):
    net_tax = tax - subsidy  # 순세금

    # 원래 균형점 계산: Qd = Qs일 때 P, Q 값
    p_eq = (a - c) / (b + d)
    q_eq = a - b * p_eq

    # 정부 개입 후 균형점 (공급곡선 이동)
    p_new = (a - c + d * net_tax) / (b + d)
    q_new = a - b * p_new

    # 다양한 가격 범위 생성
    prices = np.linspace(0, max(p_eq, p_new, price_control if price_control else 0) + 20, 500)
    qd = a - b * prices  # 수요곡선
    qs = c + d * prices  # 공급곡선
    qs_new = c + d * (prices - net_tax)  # 세금/보조금 적용 공급곡선

    # ✅ 그래프 생성 시작
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(qd, prices, label='수요곡선', color='blue')
    ax.plot(qs, prices, label='공급곡선', color='green')

    if tax != 0 or subsidy != 0:
        ax.plot(qs_new, prices, '--', label='정부개입 후 공급곡선', color='red')

    ax.scatter(q_eq, p_eq, color='purple', label=f'원래 균형 ({q_eq:.1f}, {p_eq:.1f})')
    if tax != 0 or subsidy != 0:
        ax.scatter(q_new, p_new, color='orange', label=f'개입 후 균형 ({q_new:.1f}, {p_new:.1f})')

    # ✅ 잉여 영역 시각화
    cs = consumer_surplus(a, b, p_eq, q_eq)
    ps = producer_surplus(c, d, p_eq, q_eq)

    # 소비자 잉여 삼각형 (곡선 시작점 기준)
    p_max = a / b
    cs_triangle = Polygon([[0, p_max], [q_eq, p_eq], [0, p_eq]], closed=True,
                           facecolor='skyblue', alpha=0.3, label=f'소비자 잉여: {cs:.1f}')
    ax.add_patch(cs_triangle)

    # 생산자 잉여 삼각형 (곡선 시작점 기준)
    p_min = -c / d
    ps_triangle = Polygon([[0, p_min], [q_eq, p_eq], [0, p_eq]], closed=True,
                           facecolor='lightgreen', alpha=0.3, label=f'생산자 잉여: {ps:.1f}')
    ax.add_patch(ps_triangle)

    # ✅ 정부 가격 통제선 표시 및 초과수요/공급
    if price_control_type in ['ceiling', 'floor'] and price_control is not None:
        ax.axhline(price_control, color='darkred', linestyle=':', linewidth=2, label=f'{"최고가격제" if price_control_type == "ceiling" else "최저가격제"}: {price_control}')
        surplus_type, amount = calculate_surplus_shortage(a, b, c, d, price_control)
        ax.text(0.5, price_control + 1, f'{surplus_type}: {amount:.1f}', transform=ax.get_yaxis_transform(), fontsize=10, color='darkred')

    # ✅ 그래프 마무리 설정
    ax.set_xlabel('수량 (Q)')
    ax.set_ylabel('가격 (P)')
    ax.set_title('갑국 상품 A 시장 시뮬레이션')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()

# ✅ 사용자 입력 부분 (실행 시 작동)
if __name__ == '__main__':
    print("🟢 갑국 상품 A 시장 시뮬레이션 🟢")
    a = float(input("수요 절편 a: "))        # 예: 100
    b = float(input("수요 기울기 b: "))      # 예: 2
    c = float(input("공급 절편 c: "))        # 예: 10
    d = float(input("공급 기울기 d: "))      # 예: 1.5
    tax = float(input("단위당 세금 (0이면 없음): "))  # 예: 5
    subsidy = float(input("단위당 보조금 (0이면 없음): ")) # 예: 0

    control_type_input = input("가격 통제 유형 (ceiling/최고, floor/최저, 없음): ").strip().lower()
    if control_type_input in ['ceiling', '최고']:
        control_type = 'ceiling'
        control_value = float(input("최고가격 입력: "))
    elif control_type_input in ['floor', '최저']:
        control_type = 'floor'
        control_value = float(input("최저가격 입력: "))
    else:
        control_type = None
        control_value = None

    simulate_market(a, b, c, d, tax, subsidy, control_type, control_value)
