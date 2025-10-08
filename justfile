[private]
@list:
  just --list

[group("show")]
@show_v37 *FLAGS:
  uv run render.py hdf-37.rc {{FLAGS}}

[group("show")]
@show_tnnt *FLAGS:
  uv run render.py hdf-tnnt.rc {{FLAGS}}

[group("upload")]
@v37 *FLAGS:
  uv run render.py hdf-37.rc -v nethack {{FLAGS}}

[group("upload")]
@tnnt *FLAGS:
  uv run render.py hdf-tnnt.rc -v tnnt {{FLAGS}}

[group("upload")]
all *FLAGS: (v37 FLAGS) (tnnt FLAGS)
