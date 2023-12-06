from dataclasses import dataclass, field


@dataclass
class LK:
    lk_id: str = ''
    tlg: str = ''
    date_tlg: str = ''
    srok_tlg: str = ''
    opisanie: str = ''
    lk: str = ''
    otvet: str = ''
    date_otvet: str = ''
    komu_planes: list = field(default_factory=list)
    komu_spec: list = field(default_factory=list)
    complete: int = 0
