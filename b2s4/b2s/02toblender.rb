def to_blender
  "Execute To Blender functionality."
  model = Sketchup.active_model
  show_summary = true
  status = model.export('blendsu/toblender.glb',show_summary)
end