# Do not change anything about the imports unless you know what you do
import pkgutil
import orjson
from typing import TYPE_CHECKING
from types import ModuleType

if TYPE_CHECKING:
    try:
        from worlds.pokemon_bw.ndspy.rom import NintendoDSRom
        from worlds.pokemon_bw.rom import PokemonBWPatch
    except:
        pass


# This has to exactly be named "Plugin" and needs to have a "name" field and a "patch" method
class Plugin:

    # name is unused atm, but better set it to the same as in archipelago.json
    name = "Pokemon BW QoL Plugin"

    # "rom" is the, well, ROM, but unpacked instead of raw bytes
    # "bw_patch_instance" is the class that is responsible for the standard patches
    # "files_dump" is used for dumping any file that was patched into a zip folder for debugging (enabled via host.yaml setting)
    # "plugins" is a list of all other plugin modules, in case you have to account for certain other plugins being loaded
    @staticmethod
    def patch(rom: "NintendoDSRom", bw_patch_instance: "PokemonBWPatch", files_dump: dict[str, bytes | bytearray],
              plugins: list[tuple[str, ModuleType]]):
        from worlds.pokemon_bw.ndspy.code import saveOverlayTable, codeCompression
        from worlds.pokemon_bw.ndspy.narc import NARC
        from worlds.pokemon_bw.patch import otpp

        slot_data = orjson.loads(bw_patch_instance.files.get("slot_data.json", b'{}'))
        options: dict[str, Any] = slot_data.get("options", {})
        plugin_options: dict[str, Any] = options.get("plugin_options", {})
        qol_options: dict[str, Any] = plugin_options.get("qol", {})

# Instant Text
        arm9 = bytearray(codeCompression.decompress(rom.arm9))
        if rom.name[:9] == b'POKEMON\x20W':
            arm9[0x18fda:0x18fe0] = b'\x00\x28\xc0\x46\xc0\x46'
            arm9[0x19090:0x19098] = b'\x00\x48\x00\x47\x39\x05\x0a\x02'
            extra_code = pkgutil.get_data(__name__, "files/w_insta_text_append.bin")
            arm9[0x9c538:0x9c538+len(extra_code)] = extra_code
        else:
            arm9[0x18fc0:0x18fc4] = b'\xc0\x46\xc0\x46'
            arm9[0x19074:0x1907c] = b'\x00\x48\x00\x47\x21\x05\x0a\x02'
            extra_code = pkgutil.get_data(__name__, "files/b_insta_text_append.bin")
            arm9[0x9c520:0x9c520+len(extra_code)] = extra_code
        arm9 = bytearray(codeCompression.compress(arm9, True))
        arm9[0xfc4:0xfc7] = (len(arm9) + 0x4000).to_bytes(3, "little")
        rom.arm9 = bytes(arm9)
        files_dump["arm9"] = rom.arm9

# Faster Story
        narc = NARC(rom.getFileByName("a/0/0/3"))
        for i in [82, 349, 353, 361, 428, 429, 435, 436]:
            loaded_file = pkgutil.get_data(__name__, f"files/a003/a003_{i:03d}")
            narc.files[i] = otpp.patch(narc.files[i], loaded_file)
            files_dump[f"a003/{i}"] = narc.files[i]
        rom.setFileByName("a/0/0/3", narc.save())

        narc = NARC(rom.getFileByName("a/0/5/7"))
        for i in [12, 14, 18, 20, 32, 34, 36, 38, 58, 62, 124, 126, 128, 154, 194, 216, 228, 242, 308, 310, 634, 638, 642, 648, 658, 778, 780, 782, 792, 794]:
            loaded_file = pkgutil.get_data(__name__, f"files/a057/a057_{i:03d}")
            narc.files[i] = otpp.patch(narc.files[i], loaded_file)
            files_dump[f"a057/{i}"] = narc.files[i]
        rom.setFileByName("a/0/5/7", narc.save())

        narc = NARC(rom.getFileByName("a/1/2/5"))
        for i in [16, 28, 62, 154, 155, 321]:
            loaded_file = pkgutil.get_data(__name__, f"files/a125/a125_{i:03d}")
            narc.files[i] = otpp.patch(narc.files[i], loaded_file)
            files_dump[f"a125/{i}"] = narc.files[i]
        rom.setFileByName("a/1/2/5", narc.save())

# Field Moves
        narc1 = NARC(rom.getFileByName("a/0/0/3"))
        narc2 = NARC(rom.getFileByName("a/0/5/7"))
        match qol_options.get("hm_use", False):
            case "fast":
                suffix = "fast"
            case "fastest":
                suffix = "fastest"
            case _:
                suffix = "rock_smash"
        loaded_file = pkgutil.get_data(__name__, f"files/a003/a003_280_{suffix}")
        narc1.files[280] = otpp.patch(narc1.files[280], loaded_file)
        files_dump["a003/280"] = narc1.files[280]
        rom.setFileByName("a/0/0/3", narc1.save())
        loaded_file = pkgutil.get_data(__name__, f"files/a057/a057_867_{suffix}")
        narc2.files[867] = otpp.patch(narc2.files[867], loaded_file)
        files_dump["a057/867"] = narc2.files[867]
        rom.setFileByName("a/0/5/7", narc2.save())

# Guaranteed Fishing
        narc = NARC(rom.getFileByName("a/1/2/6"))
        for i in [0, 1, 2, 6, 49, 53, 58, 69, 71, 72, 73, 75, 77, 79, 80, 81, 82, 84, 93, 94, 98, 101, 103, 104, 105, 108, 109, 110, 111]:
            loaded_file = pkgutil.get_data(__name__, f"files/a126/a126_{i:03d}")
            narc.files[i] = otpp.patch(narc.files[i], loaded_file)
            files_dump[f"a126/{i}"] = narc.files[i]
        rom.setFileByName("a/1/2/6", narc.save())

# Bike Everywhere / Remove Surf & Bike Music
        narc = NARC(rom.getFileByName("a/0/1/2"))
        loaded_bike = pkgutil.get_data(__name__, "files/a012/a012_000_bike")
        loaded_music = pkgutil.get_data(__name__, "files/a012/a012_000_music")
        narc.files[0] = otpp.patch(otpp.patch(narc.files[0], loaded_bike), loaded_music)
        files_dump["a012/0"] = narc.files[0]
        rom.setFileByName("a/0/1/2", narc.save())

# Gym Warps
        narc = NARC(rom.getFileByName("a/0/0/8"))
        for i in [515, 518, 519, 520, 524, 525, 527, 538, 548, 552, 564, 565, 595, 606, 615]:
            loaded_file = pkgutil.get_data(__name__, f"files/a008/a008_{i:03d}")
            narc.files[i] = otpp.patch(narc.files[i], loaded_file)
            files_dump[f"a008/{i}"] = narc.files[i]
        rom.setFileByName("a/0/0/8", narc.save())

        narc = NARC(rom.getFileByName("a/1/2/5"))
        for i in [7, 18, 19, 29, 63, 97, 98, 108, 114, 121]:
            loaded_file = pkgutil.get_data(__name__, f"files/a125/a125_{i:03d}")
            narc.files[i] = otpp.patch(narc.files[i], loaded_file)
            files_dump[f"a125/{i}"] = narc.files[i]
        rom.setFileByName("a/1/2/5", narc.save())

# No Pickup Animation & Fanfare Skip
        narc = NARC(rom.getFileByName("a/0/5/7"))
        for i in [862, 864]:
            loaded_file = pkgutil.get_data(__name__, f"files/a057/a057_{i:03d}")  # not hardcoded _862
            narc.files[i] = otpp.patch(narc.files[i], loaded_file)
            files_dump[f"a057/{i}"] = narc.files[i]
        rom.setFileByName("a/0/5/7", narc.save())

# Always On (Repel Prompt, Shortcuts, Delete 4)
        narc = NARC(rom.getFileByName("a/0/0/3"))
        for i in [82, 141, 263, 267, 268, 300]:
            loaded_file = pkgutil.get_data(__name__, f"files/a003/a003_{i:03d}")
            narc.files[i] = otpp.patch(narc.files[i], loaded_file)
            files_dump[f"a003/{i}"] = narc.files[i]
        rom.setFileByName("a/0/0/3", narc.save())

        narc = NARC(rom.getFileByName("a/0/5/7"))
        for i in [272, 292, 502, 504, 528, 554, 556, 872]:
            loaded_file = pkgutil.get_data(__name__, f"files/a057/a057_{i:03d}")
            narc.files[i] = otpp.patch(narc.files[i], loaded_file)
            files_dump[f"a057/{i}"] = narc.files[i]
        rom.setFileByName("a/0/5/7", narc.save())

        narc = NARC(rom.getFileByName("a/1/2/5"))
        for i in [251, 252, 264, 277]:
            loaded_file = pkgutil.get_data(__name__, f"files/a125/a125_{i:03d}")
            narc.files[i] = otpp.patch(narc.files[i], loaded_file)
            files_dump[f"a125/{i}"] = narc.files[i]
        rom.setFileByName("a/1/2/5", narc.save())
