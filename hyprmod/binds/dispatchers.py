"""Dispatcher categories, bind type metadata, and display helpers.

UI presentation data for Hyprland dispatchers and bind types — icons,
labels, categories, and human-readable formatting.
"""

from typing import TypedDict

from hyprmod.i18n import N_, _

# ---------------------------------------------------------------------------
# Bind types
# ---------------------------------------------------------------------------


class BindTypeInfo(TypedDict):
    """Metadata for a bind type (e.g. ``bind``, ``binde``)."""

    label: str
    desc: str


BIND_TYPES: dict[str, BindTypeInfo] = {
    "bind": {"label": N_("Normal"), "desc": N_("Triggers on key press")},
    "binde": {"label": N_("Repeat"), "desc": N_("Repeats while held (volume, resize)")},
    "bindm": {"label": N_("Mouse"), "desc": N_("Mouse button bind (move/resize)")},
    "bindl": {"label": N_("Locked"), "desc": N_("Works even when screen is locked")},
    "bindr": {"label": N_("Release"), "desc": N_("Triggers on key release")},
    "bindn": {"label": N_("Non-consuming"), "desc": N_("Key event passes through to windows")},
}

# Bind types selectable when the dialog's trigger mode is "Key combination".
# ``bindm`` is excluded because it's reached via the dedicated "Mouse button"
# trigger mode instead.
KEY_BIND_TYPES: dict[str, BindTypeInfo] = {k: v for k, v in BIND_TYPES.items() if k != "bindm"}

# ---------------------------------------------------------------------------
# Mouse buttons & bindm-specific dispatchers
# ---------------------------------------------------------------------------


# Friendly preset list for the mouse-drag button picker. The bare
# ``mouse:N`` strings on the left are Hyprland's wire format.
MOUSE_BUTTON_PRESETS: list[tuple[str, str]] = [
    ("mouse:272", N_("Left button")),
    ("mouse:273", N_("Right button")),
    ("mouse:274", N_("Middle button")),
    ("mouse:275", N_("Back")),
    ("mouse:276", N_("Forward")),
]

MOUSE_BUTTON_LABELS: dict[str, str] = dict(MOUSE_BUTTON_PRESETS)


# Linux input event button codes for ``GtkGestureClick`` (button 1 = left,
# 2 = middle, 3 = right, 8 = back, 9 = forward) mapped onto Hyprland's
# ``mouse:NNN`` evdev codes (272 + N - 1 for the standard buttons,
# 275/276 for the side buttons). Used by the Record button to translate a
# captured click into the wire format.
GDK_BUTTON_TO_MOUSE_KEY: dict[int, str] = {
    1: "mouse:272",  # Left
    2: "mouse:274",  # Middle
    3: "mouse:273",  # Right
    8: "mouse:275",  # Back
    9: "mouse:276",  # Forward
}


# Dispatchers that make sense for ``bindm`` (mouse drag). These overlap with
# entries in "Window Management" and "Focus and Move Windows" — the same
# dispatcher name behaves differently as a key vs mouse bind, so the
# bindm-only label set is kept separate from ``DISPATCHER_INFO`` to avoid
# clobbering the keyboard variant in the flat lookup.
BINDM_DISPATCHERS: dict[str, str] = {
    "movewindow": N_("Move window"),
    "resizewindow": N_("Resize window"),
}

# ---------------------------------------------------------------------------
# Dispatcher category system
# ---------------------------------------------------------------------------


class DispatcherInfo(TypedDict):
    """Metadata for a single dispatcher."""

    label: str
    arg_type: str


class DispatcherInfoWithCategory(DispatcherInfo):
    """Dispatcher metadata augmented with its category id."""

    category_id: str


class DispatcherCategory(TypedDict):
    """A group of related dispatchers."""

    id: str
    label: str
    icon: str
    dispatchers: dict[str, DispatcherInfo]


DISPATCHER_CATEGORIES: list[DispatcherCategory] = [
    {
        "id": "apps",
        "label": N_("Launch Application"),
        "icon": "system-run-symbolic",
        "dispatchers": {
            "exec": {"label": N_("Run command"), "arg_type": "command"},
            "execr": {"label": N_("Run raw command"), "arg_type": "command"},
        },
    },
    {
        "id": "window_mgmt",
        "label": N_("Window Management"),
        "icon": "overlapping-windows-symbolic",
        "dispatchers": {
            "killactive": {"label": N_("Close window"), "arg_type": "none"},
            "forcekillactive": {"label": N_("Force kill window"), "arg_type": "none"},
            "togglefloating": {"label": N_("Toggle floating"), "arg_type": "none"},
            "fullscreen": {"label": N_("Toggle fullscreen"), "arg_type": "fullscreen_mode"},
            "pin": {"label": N_("Pin window"), "arg_type": "none"},
            "centerwindow": {"label": N_("Center window"), "arg_type": "none"},
            "pseudo": {"label": N_("Toggle pseudo-tiling"), "arg_type": "none"},
            "layoutmsg": {"label": N_("Layout message"), "arg_type": "text"},
        },
    },
    {
        "id": "workspace_nav",
        "label": N_("Workspace Navigation"),
        "icon": "shell-overview-symbolic",
        "dispatchers": {
            "workspace": {"label": N_("Switch workspace"), "arg_type": "workspace"},
            "movetoworkspace": {
                "label": N_("Move window to workspace"),
                "arg_type": "workspace",
            },
            "movetoworkspacesilent": {
                "label": N_("Move window silently"),
                "arg_type": "workspace",
            },
            "togglespecialworkspace": {
                "label": N_("Toggle scratchpad"),
                "arg_type": "optional_text",
            },
        },
    },
    {
        "id": "window_focus",
        "label": N_("Focus and Move Windows"),
        "icon": "move-to-window-symbolic",
        "dispatchers": {
            "movefocus": {"label": N_("Move focus"), "arg_type": "direction"},
            "movewindow": {"label": N_("Move window"), "arg_type": "direction"},
            "swapwindow": {"label": N_("Swap window"), "arg_type": "direction"},
            "movewindoworgroup": {
                "label": N_("Move window or group"),
                "arg_type": "direction",
            },
            "resizeactive": {"label": N_("Resize window"), "arg_type": "resize"},
            "cyclenext": {"label": N_("Cycle focus next"), "arg_type": "none"},
            "swapnext": {"label": N_("Swap with next"), "arg_type": "none"},
            "focuscurrentorlast": {"label": N_("Focus last window"), "arg_type": "none"},
            "focusurgentorlast": {"label": N_("Focus urgent/last"), "arg_type": "none"},
        },
    },
    {
        "id": "mouse_button",
        "label": N_("Mouse Button"),
        "icon": "input-mouse-symbolic",
        # Empty: ``movewindow`` / ``resizewindow`` already live in
        # "Focus and Move Windows" / "Window Management", and the flat
        # ``DISPATCHER_INFO`` lookup can only hold one category per
        # dispatcher name. The dialog reads ``BINDM_DISPATCHERS`` directly
        # when the trigger mode is "Mouse button".
        "dispatchers": {},
    },
    {
        "id": "grouping",
        "label": N_("Window Grouping"),
        "icon": "group-symbolic",
        "dispatchers": {
            "togglegroup": {"label": N_("Toggle group"), "arg_type": "none"},
            "changegroupactive": {
                "label": N_("Cycle group member"),
                "arg_type": "group_dir",
            },
            "moveoutofgroup": {"label": N_("Remove from group"), "arg_type": "none"},
            "moveintogroup": {"label": N_("Move into group"), "arg_type": "direction"},
            "movegroupwindow": {"label": N_("Reorder in group"), "arg_type": "group_dir"},
            "lockgroups": {"label": N_("Lock all groups"), "arg_type": "text"},
            "lockactivegroup": {"label": N_("Lock active group"), "arg_type": "text"},
            "denywindowfromgroup": {
                "label": N_("Deny window from group"),
                "arg_type": "text",
            },
        },
    },
    {
        "id": "monitor",
        "label": N_("Monitor Control"),
        "icon": "preferences-desktop-display-symbolic",
        "dispatchers": {
            "focusmonitor": {"label": N_("Focus monitor"), "arg_type": "text"},
            "movecurrentworkspacetomonitor": {
                "label": N_("Move workspace to monitor"),
                "arg_type": "text",
            },
            "moveworkspacetomonitor": {
                "label": N_("Move specific workspace to monitor"),
                "arg_type": "text",
            },
            "swapactiveworkspaces": {
                "label": N_("Swap workspaces between monitors"),
                "arg_type": "text",
            },
            "focusworkspaceoncurrentmonitor": {
                "label": N_("Focus workspace on current monitor"),
                "arg_type": "workspace",
            },
            "dpms": {"label": N_("Screen on/off"), "arg_type": "dpms"},
        },
    },
    {
        "id": "session",
        "label": N_("Session"),
        "icon": "computer-symbolic",
        "dispatchers": {
            "exit": {"label": N_("Exit Hyprland"), "arg_type": "none"},
            "pass": {"label": N_("Pass key to window"), "arg_type": "text"},
            "global": {"label": N_("Global shortcut"), "arg_type": "text"},
            "submap": {"label": N_("Enter submap"), "arg_type": "text"},
        },
    },
    {
        "id": "advanced",
        "label": N_("Other"),
        "icon": "terminal-symbolic",
        "dispatchers": {},
    },
]


# Flat lookups derived from DISPATCHER_CATEGORIES at import time.
CATEGORY_BY_ID: dict[str, DispatcherCategory] = {cat["id"]: cat for cat in DISPATCHER_CATEGORIES}
DISPATCHER_INFO: dict[str, DispatcherInfoWithCategory] = {
    dname: {**dinfo, "category_id": cat["id"]}
    for cat in DISPATCHER_CATEGORIES
    for dname, dinfo in cat["dispatchers"].items()
}


def categorize_dispatcher(dispatcher: str) -> str:
    """Return category id for a dispatcher, defaulting to 'advanced'."""
    info = DISPATCHER_INFO.get(dispatcher)
    return info["category_id"] if info else "advanced"


def categorize_bind(bind_type: str, dispatcher: str) -> str:
    """Return category id for a bind.

    ``bindm`` always categorises as ``mouse_button`` regardless of dispatcher,
    because ``movewindow``/``resizewindow`` also exist as keyboard
    dispatchers (with a directional argument) and would otherwise be
    bucketed alongside their key-mode siblings.
    """
    if bind_type == "bindm":
        return "mouse_button"
    return categorize_dispatcher(dispatcher)


def dispatcher_label(dispatcher: str) -> str:
    """Human-readable label for a dispatcher."""
    info = DISPATCHER_INFO.get(dispatcher)
    return _(info["label"]) if info else dispatcher


def bind_dispatcher_label(bind_type: str, dispatcher: str) -> str:
    """Human-readable label for a bind's dispatcher.

    Uses ``BINDM_DISPATCHERS`` when ``bind_type == "bindm"`` so mouse-drag
    binds read as "Move window" / "Resize window" instead of the
    direction-flavoured keyboard label.
    """
    if bind_type == "bindm" and dispatcher in BINDM_DISPATCHERS:
        return _(BINDM_DISPATCHERS[dispatcher])
    return _(dispatcher_label(dispatcher))


def format_action(dispatcher: str, arg: str) -> str:
    """Human-readable action string: ``'Run command: firefox'`` or ``'Close window'``."""
    label = _(dispatcher_label(dispatcher))
    if arg:
        return f"{label}: {arg}"
    return label


def format_bind_action(bind_type: str, dispatcher: str, arg: str) -> str:
    """Human-readable action string for a bind, with bindm-specific labels."""
    label = _(bind_dispatcher_label(bind_type, dispatcher))
    if arg:
        return f"{label}: {arg}"
    return label
