from pydantic import BaseModel, Field


class LevelResources(BaseModel):
    """
    :param power_points: POWERPOINTS
    :param gold: GOLD
    """

    power_points: int
    gold: int


class Level(BaseModel):
    """
    :param level_n: POWERPOINTS + GOLD
    """

    level_2: LevelResources
    level_3: LevelResources
    level_4: LevelResources
    level_5: LevelResources
    level_6: LevelResources
    level_7: LevelResources
    level_8: LevelResources
    level_9: LevelResources
    level_10: LevelResources
    level_11: LevelResources


class Gears(BaseModel):
    """
    :param gear: GOLD
    """

    gadget: int
    normal_gears: int
    epic_gears: int
    mythic_gears: int
    starpower: int
    hypercharge: int


class GamblingResources(BaseModel):
    """
    :param power_points: POWERPOINTS
    :param gold: GOLD
    """

    power_points: int
    gold: int


class BuffiesResources(BaseModel):
    """
    :param gambling: POWERPOINT + GOLD
    :param gems: GEMS
    """

    gambling: GamblingResources
    gems: int


class LevelUpResources(BaseModel):
    """
    :param level: LEVEL, POWERPOINT + GOLD
    :param gears: GEARS
    :param buffies: POIWERPOINT + GOLD || GEMS
    """

    levels: Level
    gears: Gears
    buffies: BuffiesResources


# --- USER DATA ---


class BrawlerLevelUp(BaseModel):
    resources: LevelUpResources

    initial_level: int = Field(default=1, gt=0)
    target_level: int = Field(default=11, gt=1)

    gadget_amount: int = Field(default=0)
    normal_gear_amount: int = Field(default=0)
    epic_gear_amount: int = Field(default=0)
    mythic_gear_amount: int = Field(default=0)
    starpower_amount: int = Field(default=0)
    hypercharge: bool = Field(default=False)

    @property
    def level_resources(self):
        levels: dict[int, LevelResources] = {
            2: self.resources.levels.level_2,
            3: self.resources.levels.level_3,
            4: self.resources.levels.level_4,
            5: self.resources.levels.level_5,
            6: self.resources.levels.level_6,
            7: self.resources.levels.level_7,
            8: self.resources.levels.level_8,
            9: self.resources.levels.level_9,
            10: self.resources.levels.level_10,
            11: self.resources.levels.level_11,
        }

        resources = {
            "power_points": 0,
            "gold": 0,
        }

        for count in range(self.initial_level + 1, self.target_level + 1):
            resources["power_points"] += levels[count].power_points
            resources["gold"] += levels[count].gold

        return LevelResources(**resources)

    @property
    def gear_resources(self) -> int:
        gadget_resources = self._gadget_resources

        normal_gear_resources = self._normal_gear_resources
        epic_gear_resources = self._epic_gear_resources
        mythic_gear_resources = self._mythic_gear_resources

        starpower_resources = self._starpower_resources

        hypercharge = (
            self.resources.gears.hypercharge if self.hypercharge is not False else 0
        )

        return (
            gadget_resources
            + normal_gear_resources
            + epic_gear_resources
            + mythic_gear_resources
            + starpower_resources
            + hypercharge
        )

    @property
    def _gadget_resources(self) -> int:
        return self.resources.gears.gadget * self.gadget_amount

    @property
    def _normal_gear_resources(self) -> int:
        return self.resources.gears.normal_gears * self.normal_gear_amount

    @property
    def _epic_gear_resources(self) -> int:
        return self.resources.gears.epic_gears * self.epic_gear_amount

    @property
    def _mythic_gear_resources(self) -> int:
        return self.resources.gears.mythic_gears * self.mythic_gear_amount

    @property
    def _starpower_resources(self) -> int:
        return self.resources.gears.starpower * self.starpower_amount
