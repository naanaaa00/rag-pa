import { type RouteConfig, index, layout, route } from "@react-router/dev/routes";

export default [
  layout("routes/_layout.tsx", [
    index("routes/home.tsx"),
    layout("routes/dashboard/_layout.tsx", [
      route("dashboard", "routes/dashboard/_index.tsx"),
      route("notes", "routes/notes/_index.tsx"),
      route("notes/new", "routes/notes/new.tsx"),
      route("notes/:noteId", "routes/notes/$noteId.tsx"),
      route("voice", "routes/voice/_index.tsx"),
      route("voice/record", "routes/voice/record.tsx"),
    ]),
  ])
] satisfies RouteConfig;
