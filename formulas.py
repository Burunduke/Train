#  1 и 2 листы, в 4 листе trans_coef = 1
def stationary_fuel_burn(fuel_consumption: dict, fuel_emissions: dict, oxi_coef: dict, trans_coef: dict) -> (
        float, dict):
    """
    Стационарное сжигание топлива (РФ)
    :param fuel_consumption: словарь расхода j-топлива за период, тыс. т
    :param fuel_emissions: словарь коэффициентов выбросов СО2 от сжигания j-топлива за период, тСО2/ТДж
    :param oxi_coef: словарь коэффициентов окисления j-топлива, доля
    :param trans_coef: Коэффициент перевода в энергетические единицы, ТДж/тыс.т
    :return: общая сумма и словарь выбросов СО2 от стационарного сжигания j-топлива за период, тСО2
    """
    res = 0
    total_emissions = {}
    for j in fuel_consumption:
        total_emissions.update({j: fuel_consumption[j] * fuel_emissions[j] * oxi_coef[j] * trans_coef[j]})
        res += total_emissions[j]

    return res, total_emissions


#  3 лист
def stationary_gas_coef(other_comps: dict, comps_chem: dict) -> ():
    """
    Расчет коэффициента выбросов СО2 при сжигании топлива на стационарных источниках по компонентному составу
    :param other_comps: словарь содержания i-компонентов, в j-углеводородной смеси, % об
    :param comps_chem: словарь количества молей углерода на моль i-компонента j-углеводородной смеси
    :return: Коэффициент выбросов СО2 от сжигания газообразного топлива j за период
    """
    res = 0
    for i in other_comps:
        res += other_comps[i] * comps_chem[i]

    return 1.8393 * res  # rho(CO2)


#
def stationary_gas_burn(fuel_consumption: dict, fuel_emissions: dict, oxi_coef: dict, trans_coef: dict) -> (
        float, dict):
    """
    Стационарное сжигание топлива (РФ)
    :param fuel_consumption: словарь расхода j-топлива за период, тыс. т
    :param fuel_emissions: словарь коэффициентов выбросов СО2 от сжигания j-топлива за период, тСО2/ТДж
    :param oxi_coef: словарь коэффициентов окисления j-топлива, доля
    :param trans_coef: Коэффициент перевода в энергетические единицы, ТДж/тыс.т
    :return: общая сумма и словарь выбросов СО2 от стационарного сжигания j-топлива за период, тСО2
    """
    res = 0
    total_emissions = {}
    for j in fuel_consumption:
        total_emissions.update({j: fuel_consumption[j] * fuel_emissions[j] * oxi_coef[j] * trans_coef[j]})
        res += total_emissions[j]

    return res, total_emissions


#  лист 6
def torch_fuel_coef(CO2_content_coef: float, other_comps: dict, comps_chem: dict, unburn_coef: float,
                    CH4_content_coef: float, rho_CO2: float, rho_CH4: float) -> dict:
    """
    Стационарное сжигание топлива в факелах (РФ)
    :param rho_CO2:
    :param rho_CH4:
    :param CO2_content_coef: словарь содержания CO2 в j-углеводородных смесей за период, % об
    :param other_comps: словарь содержания i-компонентов, кроме CO2, в j-углеводородной смеси, % об
    :param comps_chem: словарь количества молей углерода на моль i-компонента j-углеводородной смеси;
    :param unburn_coef: словарь коэффициентов недожога j-углеводородной смеси на факельной установке за период, доля
    :param CH4_content_coef: словарь содержания CO2 в j-углеводородных смесей за период, % об
    :return total_coefs: словарь коэффициентов CO2/CH4 от сжигания всех углеводородных смесей на факельной установке за период
    """

    total_coefs = {}
    #  CO2
    res = 0
    for i in other_comps:
        res += other_comps[i] * comps_chem[i]
    res = (CO2_content_coef + res * (1 - unburn_coef)) * rho_CO2 / 100
    total_coefs.update({"CO2": res})

    #  CH4
    res = CH4_content_coef * unburn_coef * rho_CH4  # rho(CH4) * 10**(-2) = 0.0657 * 0.01
    total_coefs.update({"CH4": res})

    return total_coefs


#  лист 5 без выбросов (считается в конце)
def torch_fuel_burn(fuel_consumption: dict, CO2_coef: dict, CH4_coef: dict) -> dict:
    """
    Стационарное сжигание топлива в факелах (РФ)
    :param fuel_consumption: словарь расходов j-углеводородных смесей на факельной установке за период, тыс. м3
    :param CO2_coef: словарь содержания CO2 в j-углеводородных смесей за период, % об
    :param CH4_coef: словарь содержания CO2 в j-углеводородных смесей за период, % об
    :return total_emissions: словарь выбросов CO2/CH4 от сжигания всех углеводородных смесей на факельной установке за период
    """
    total_emissions = {}
    #  CO2
    res = 0
    for j in fuel_consumption:
        res += fuel_consumption[j] * CO2_coef[j]
    total_emissions.update({"CO2": res})

    #  CH4
    res = 0
    for j in fuel_consumption:
        res += fuel_consumption[j] * CH4_coef[j]
    total_emissions.update({"CH4": res})

    return total_emissions


#  лист 7
def fugitive_emissions(fuel_consumption: dict, CO2_content_coef: dict, CH4_content_coef: dict) -> dict:
    """
    Фугитивные выбросы
    :param fuel_consumption: расход j-углеводородной смеси на технологические операции (объем отведения
без сжигания) за период y, тыс. м3
    :param CO2_content_coef: содержание СО2 в смеси j за период y, % об
    :param CH4_content_coef: содержание СН4 в смеси j за период y, % об
    :return: фугитивные выбросы i-парникового газа за период y, т;
    """
    res_CO2 = 0
    res_CH4 = 0
    for j in fuel_consumption:
        res_CO2 += fuel_consumption[j] * CO2_content_coef[j]
        res_CH4 += fuel_consumption[j] * CH4_content_coef[j]
    total_emissions = {
        "CO2": res_CO2,
        "CH4": res_CH4
    }
    return total_emissions


#  лист 8
def waste_water_CH4(B0: int, corr_coef: dict, volume: dict, organic_coef: dict, organic_waste: dict) -> (dict, float):
    """
    Очистка и сброс сточных вод
    :param organic_coef: Концентрация органических веществ в сточных водах, Cj, г БПК/м3
    :param volume: Объем очищаемых или сбрасываемых сточных вод, Vj, м3
    :param B0: максимальная способность образования CH4, кг CH4/кг БПК
    :param corr_coef: поправочный коэффициент для метана (дробь)
    :param organic_waste: количество органического компонента, удаленного как отстой кг ХПК/год


    :return: словарь выбросов метана (бытовых и индустриальных)
    """
    res = {}
    emission_coef = {}  # Коэффициент выбросов, кг СН4/кг БПК
    biodegradable = {}  # масса органических веществ в сточных водах системы jj, БПК кг/год;
    for j in corr_coef:
        emission_coef.update({j: B0 * corr_coef[j]})
        biodegradable.update({j: volume[j] * organic_coef[j] * 0.001})
        res.update({j: (biodegradable[j] - organic_waste[j]) * emission_coef[j]})

    return res, sum(res.values())


# лист 8
def wastewater_N2O(prot: dict, N_waste: dict, N_coef=0.16, uncons_prot=1.2, ind_prot=1.25, waste_coef=0.05,
                   trans_coef=(44 / 28)) -> (dict, float):
    """
    Выбросы закиси азота из сточных вод
    :param prot: годовое потребление протеина на душу населения, кг/год
    :param N_coef: доля азота в протеине;
    :param uncons_prot: коэффициент для непотребленного протеина, сброшенного в сточные воды;
    :param ind_prot: коэффициент для промышленного и коммерческого количества протеина,
    попутно сброшенного в канализационную систему
    :param N_waste: азот, удаленный с отстоем сточных вод, кг N/год
    :param waste_coef: коэффициент выбросов N2O выбросов при сбросе сточных вод кг - N/кг N
    :param trans_coef: Коэффициент для преобразования кг N2O-N в кг N2О = 44/28
    :return: выбросы N2O от сточных вод, кг N2O/год
    """
    N_water = {}  # Общее годовое количество азота в отводе сточных вод, NСТОК, кг N/год
    res = {}
    for j in prot:
        N_water.update({j: prot[j] * N_coef * uncons_prot * ind_prot - N_waste[j]})
        res.update({j: N_water[j] * waste_coef * trans_coef})
    return res, sum(res.values())


# лист 9
def waste_burn_CO2(mass: dict, dry_coef: dict, carbon_coef: dict, fossil_coef: dict, oxi_coef: dict,
                   mixed_mass: int, comp_coef: dict, dry_comp_coef: dict, carbon_comp_coef: dict,
                   fossil_comp_coef: dict, oxi_comp_coef: dict, liquid_mass: dict,
                   fossil_liquid_coef: dict, oxi_liquid_coef: dict) -> (dict, dict, dict, float):
    """
    Сжигание отходов. CO2

    mixed (ТКО)
    :param mixed_mass: общая масса многокомпонентного отхода (влажный вес), Гг/год
    :param comp_coef: доля компонента x (по типу отходов) в отходе (во влажном весе)
    :param dry_comp_coef: доля сухого вещества в компоненте x в отходе
    :param carbon_comp_coef: доля углерода в сухом веществе (например, содержание углерода) компонента x
    :param fossil_comp_coef: доля ископаемого углерода в общем количестве углерода в компоненте x
    :param oxi_comp_coef: коэффициент окисления, (доля)

    solid
    :param mass: масса твердых отходов вида i (вес влажного вещества), Гг/год;
    :param dry_coef: доля сухого вещества в отходах (во влажном весе)
    :param carbon_coef: доля углерода в сухом веществе (общее содержание углерода) сжигаемых отходов
    :param fossil_coef: доля ископаемого углерода в общем количестве углерода сжигаемых отходов
    :param oxi_coef: коэффициент окисления, (доля)


    liquid
    :param liquid_mass: количество сожженных ископаемых жидких отходов вида i, Гг
    :param fossil_liquid_coef: доля углерода в ископаемых жидких отходах типа i
    :param oxi_liquid_coef: коэффициент окисления для ископаемых жидких отходов вида i, (доля)

    :return: Выбросы CO2 от сжигания твердых отходов.
    """
    res = 0
    #  mixed
    mixed = {}
    for x in comp_coef:
        temp = mixed_mass * comp_coef[x] * dry_comp_coef[x] * carbon_comp_coef[x] * \
               fossil_comp_coef[x] * oxi_comp_coef[x] * 44 / 12
        mixed.update({x: temp})
        res += temp

    #  solid
    solid = {}
    for i in mass:
        temp = mass[i] * dry_coef[i] * carbon_coef[i] * fossil_coef[i] * oxi_coef[i] * 44 / 12
        solid.update({i: temp})
        res += temp

    #  liquid
    liquid = {}
    for i in liquid_mass:
        temp = liquid_mass[i] * fossil_liquid_coef[i] * oxi_liquid_coef[i] * 44 / 12
        liquid.update({i: temp})
        res += temp

    return mixed, solid, liquid, res


# лист 9
def waste_burn_N2O(mass: dict, emission_coef: dict) -> (dict, float):
    """
    Сжигание отходов. N20 инсернации, по надобности можно включить открытое сжигание
    :param mass: количество отходов типа i (вес влажного вещества), подвергнутого инсинерации, Гг/год
    :param emission_coef: коэффициент выбросов N2O (кг N2O /Гг отходов) для отходов типа i,
    подвергаемых инсинерации или открытому сжиганию
    :return: выбросы N2O от сжигания отходов в учитываемом в год, для которого выполняется инвентаризация, Гг/год
    """
    res = {}
    for i in mass:
        res.update({i: mass[i] * emission_coef[i] * 10 ** (-6)})

    return res, sum(res.values())


# лист 10
def transport(fuel_volume: dict, rho: dict, CO2_coef: dict) -> (dict, float):
    """
    Количественное определение впг при сжигании топлива в транспорте
    :param fuel_volume: Расход топлива вида j транспортным средством типа b за период y, выраженный в объемной величине, л
    :param rho: Плотность топлива вида j, ρj, кг/л
    :param CO2_coef: Коэффициент выбросов СО2 при использовании в транспортном средстве типа b вида топлива j т СО2/т

    :return: Выбросы СО2 от сжигания топлива в двигателях автотранспортных средств за период y, т СО2
    """
    res = {}
    fuel_consumption = {}
    for i in fuel_volume:
        fuel_consumption.update({i: fuel_volume[i] * rho[i]})
        res.update({i: fuel_consumption[i] * CO2_coef})

    return res, sum(res.values())


#  лист 11
def region_coef(other_comps: dict, comps_chem: dict, rho_CO2: float, gas_volume: float,
                gas_burn_volume: float, heat_energy: float) -> (float, float):
    """
    Расчет коэффициента выбросов СО2 при сжигании топлива на стационарных источниках по компонентному составу
    :param other_comps: Объемная доля i-компонента в газообразного топлива за период у, Wi,j,y, % об.
    :param comps_chem: Количество молей углерода на моль i-компонента газообразного топлива, nC, i
    :param rho_CO2: Плотность СО2, ρCO2, кг/м3
    :param gas_volume: Объем газа (тыс.м3)
    :param gas_burn_volume: Объем газа (тыс.м3)
    :param heat_energy: Выработано тепловой энергии (Гкал)
    :return: Коэффициент выбросов СО2 от сжигания газообразного топлива j за период; Коэффициент (тСО2\ Гкал)
    """
    #  CO2
    coef_CO2 = 0
    for i in other_comps:
        coef_CO2 += other_comps[i] * comps_chem[i]

    coef_CO2 *= rho_CO2 / 100  # Коэффициент выбросов СО2 от сжигания газообразного топлива j за период у, тСО2/тыс.м3

    #  МВт
    res_MWt = coef_CO2 * gas_volume  # ВПГ (тСО2)
    res_MWt /= 2.482  # Коэффициент (тСО2\МВт)

    #  Гкал
    res_Gcal = coef_CO2 * gas_burn_volume
    res_Gcal /= heat_energy

    return res_MWt, res_Gcal


#  лист 11
def indirect_emissions(energy_cons: dict, coef: dict) -> (dict, float):
    """
    Количественное определение объема косвенных энергетических выбросов парниковых газов
    :param energy_cons: Количественное определение объема косвенных энергетических выбросов парниковых газов
    :param coef: Региональный коэффициент косвенных энергетических выбросов, тСО2/ед

    :return: Объем косвенных энергетических выбросов при потреблении энергии, тСО2
    """
    emission_volume = {}
    for i in energy_cons:
        emission_volume.update({i: energy_cons[i] * coef})

    return emission_volume, sum(emission_volume.values())


#  лист 12
def sum_of_gas_emissions(gases: dict) -> float:
    """
    Прямые выбросы парниковых газов (РФ)
    :param gases: словарь выбросов парниковых газов (CO2, CH4, N2O, CHF3, CF4, C2F6, SF6) за период, т
    :return: сумма выбросов парниковых газов в CO2-эквиваленте за период, тCO2-эквивалента;
    """
    GWP = {
        'CO2': 1,
        'CH4': 25,
        'N2O': 298,
        'CHF3': 14800,
        'CF4': 7390,
        'C2F6': 12200,
        'SF6': 22800
    }
    res = 0
    for j in gases:
        res += gases[j] * GWP[j]

    return res
