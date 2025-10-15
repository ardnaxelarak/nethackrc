[private]
@list:
  just --list

[group("show")]
@render TEMPLATE *FLAGS:
  uv run render.py {{TEMPLATE}} {{FLAGS}}

[group("show")]
@v37 *FLAGS:
  uv run render.py hdf-37.rc {{FLAGS}}

[group("show")]
@crecelle *FLAGS:
  uv run render.py hdf-crecelle.rc {{FLAGS}}

[group("show")]
@tnnt *FLAGS:
  uv run render.py hdf-tnnt.rc {{FLAGS}}

[group("upload")]
@upload_v37 *FLAGS:
  uv run render.py hdf-37.rc -hdf_variant nethack {{FLAGS}}

[group("upload")]
@upload_tnnt *FLAGS:
  uv run render.py hdf-tnnt.rc -hdf_variant tnnt {{FLAGS}}

[group("show")]
@upload_crecelle *FLAGS:
  uv run render.py hdf-crecelle.rc -hdf_variant crecellehack {{FLAGS}}

[group("upload")]
upload_all *FLAGS: (upload_v37 FLAGS) (upload_tnnt FLAGS) (upload_crecelle FLAGS)
