n = 1
K1_values = [
    0.2566, 0.5060, 0.9170, 0.9278, 0.9328, 0.9469, 0.9555, 0.9639, 0.9706, 0.9878,
    0.9933, 1.0060, 1.0174, 1.0210, 1.0312, 1.0454, 1.0548, 1.0689, 1.0779, 1.0873,
    1.0905, 1.1007, 1.2552, 1.5072
]

K2_values = [
    0.0036, 0.00685, 0.0059, 0.0078, 0.00367, 0.0020, 0.0008, 0.0077, 0.0021, 0.0038,
    0.0055, 0.0022, 0.0064, 0.0048, 0.0015, 0.0078, 0.0010, 0.0029, 0.0023, 0.0053,
    0.00091, 0.0040, 0.0010, 0.0011
]

K3_values = [
    0.9696, 0.8953, 0.7428, 0.7388, 0.7370, 0.7320, 0.7289, 0.7259, 0.7235, 0.7174,
    0.7155, 0.7110, 0.7071, 0.7058, 0.7023, 0.6974, 0.6942, 0.6894, 0.6864, 0.6832,
    0.6821, 0.6787, 0.6296, 0.5594
]

delta_phi_values = [
    -14.1127, -26.0650, -41.32453, -41.6331, -42.2917, -42.6754, -42.5298, -42.9757,
    -43.02771, -43.9178, -44.13616, -43.8475, -44.2330, -44.1667, -45.2780, -45.5954,
    -45.9348, -45.9242, -46.4606, -46.0062, -46.8870, -47.2079, -50.4162
]

frequencies = [n * K1 for K1 in K1_values]
input_voltages = [1 + K2 for K2 in K2_values]
output_voltages = [n * K3 for K3 in K3_values]
amplitude_transfer_ratios = [Uout / Uin for Uout, Uin in zip(output_voltages, input_voltages)]

# Расчет погрешностей
emr = 0.01


def calculate_uncertainty(U_x, coefficient_percent, emr):
    delta_percent = U_x * coefficient_percent / 100
    return delta_percent + emr * 20


def calculate_K_uncertainty(K, delta_U_out, U_out, delta_U_in, U_in):
    # Применение правила сложения погрешностей для функции отношения
    return K * 0.01 * (delta_U_out / U_out + delta_U_in / U_in)


def calculate_delta_phi(phi_x):
    return 0.0001 * phi_x  # δ_φ = 0.01% * φ_x


def calculate_Delta_phi(delta_phi, phi_x):
    return delta_phi * phi_x  # ∆_φ = δ_φ * φ_x


# Расчет погрешностей
delta_U_in_values = [calculate_uncertainty(U_in, 6, emr) for U_in in input_voltages]
delta_U_out_values = [calculate_uncertainty(U_out, 6, emr) for U_out in output_voltages]
delta_K_values = [calculate_K_uncertainty(K, dU_out, U_out, dU_in, U_in)
                  for K, dU_out, U_out, dU_in, U_in in
                  zip(amplitude_transfer_ratios, delta_U_out_values, output_voltages, delta_U_in_values,
                      input_voltages)]
delta_phi_computed = [calculate_delta_phi(phi_x) for phi_x in delta_phi_values]
Delta_phi_computed = [calculate_Delta_phi(d_phi, phi_x) for d_phi, phi_x in zip(delta_phi_computed, delta_phi_values)]

# Вывод результатов
print("Частоты:")
for i, frequency in enumerate(frequencies, 1):
    print(f"Частота {i}: {frequency:.4f} Hz")

print("\nВходные напряжения:")
for i, input_voltage in enumerate(input_voltages, 1):
    print(f"Входное напряжение {i}: {input_voltage:.4f} V")

print("\nВыходные напряжения:")
for i, output_voltage in enumerate(output_voltages, 1):
    print(f"Выходное напряжение {i}: {output_voltage:.4f} V")

print("\nАмплитудные коэффициенты передачи:")
for i, ratio in enumerate(amplitude_transfer_ratios, 1):
    print(f"Амплитудный коэффициент передачи {i}: {ratio:.4f}")

print("\nПогрешности входных напряжений:")
for i, delta_U_in in enumerate(delta_U_in_values, 1):
    print(f"∆U_вх {i}: {delta_U_in:.8f} V")

print("\nПогрешности выходных напряжений:")
for i, delta_U_out in enumerate(delta_U_out_values, 1):
    print(f"∆U_вых {i}: {delta_U_out:.8f} V")

print("\nПогрешности амплитудного коэффициента передачи:")
for i, delta_K in enumerate(delta_K_values, 1):
    print(f"∆K {i}: {delta_K:.8f}")

print("\nРезультаты измерений амплитудного коэффициента передачи:")
for i, (K, delta_K) in enumerate(zip(amplitude_transfer_ratios, delta_K_values), 1):
    print(f"Измерение {i}: K = {K:.3f} ± {delta_K:.3f}")
print("Результаты расчетов:")
print(f"{'№':>3} {'Δϕ':>10} {'δ_φ (10^-4)':>15} {'∆_φ':>15}")
for i, (phi_x, d_phi, Delta_phi) in enumerate(zip(delta_phi_values, delta_phi_computed, Delta_phi_computed), 1):
    print(f"{i:3} {phi_x:10.8f} {d_phi * 1e4:>15.8f} {Delta_phi:15.8f}")
