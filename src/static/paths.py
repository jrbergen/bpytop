from pathlib import Path


class Paths:
	"""Class which stores default/static directory/file paths"""
	DIRNAME_BPYTOP = 'bpytop'
	DIRNAME_THEMES_USER = 'themes'
	DIRNAME_THEMES_PKG = 'bpytop-themes'

	FNAME_ERROR_LOG = 'error.log'
	FNAME_CFG_BPYTOP = 'bpytop.conf'

	CONFIG_DIR_DEFAULT: Path = Path(Path.home(), '.config', DIRNAME_BPYTOP)
	CONFIG_FILE_DEFAULT: Path = Path(CONFIG_DIR_DEFAULT, FNAME_CFG_BPYTOP)

	CONFIG_DIR_BSD: Path = Path("/usr/local/etc/")
	CONFIG_FILE_BSD: Path = CONFIG_DIR_BSD / FNAME_CFG_BPYTOP

	CONFIG_DIR_OTHER_PLATFORMS: Path = Path("/etc")
	CONFIG_FILE_OTHER_PLATFORMS: Path = Path(CONFIG_DIR_OTHER_PLATFORMS,
											 FNAME_CFG_BPYTOP)


	THEME_DIR_USER: Path = CONFIG_DIR_DEFAULT / DIRNAME_THEMES_USER
	THEME_DIR_PKG: Path = Path()

	LOG_PATH_ERR: Path = Path(CONFIG_DIR_DEFAULT / FNAME_ERROR_LOG)

	@classmethod
	def make_required_dirs(cls):
		cls.make_cfg_and_theme_dir()
		cls.make_pkg_theme_dir()

	@classmethod
	def make_cfg_and_theme_dir(cls):
		try:
			cls.CONFIG_DIR_DEFAULT.mkdir(exist_ok=True)
			cls.THEME_DIR_USER.mkdir(exist_ok=True)
		except PermissionError:
			print(f'ERROR!\nNo permission to write to "{str(cls.CONFIG_DIR_DEFAULT)}" directory!')
			raise SystemExit(1)

	@classmethod
	def make_pkg_theme_dir(cls):
		tmp_theme_dir_pkg = Path(__file__).parent / cls.DIRNAME_THEMES_PKG

		if tmp_theme_dir_pkg.exists():
			cls.THEME_DIR_PKG = tmp_theme_dir_pkg
		else:
			for td in ["/usr/local/", "/usr/", "/snap/bpytop/current/usr/"]:
				if Path(td, 'share', cls.DIRNAME_BPYTOP, cls.DIRNAME_THEMES_USER).exists():
					cls.THEME_DIR_PKG = Path(td, 'share', cls.DIRNAME_BPYTOP, cls.DIRNAME_THEMES_USER)
					break
