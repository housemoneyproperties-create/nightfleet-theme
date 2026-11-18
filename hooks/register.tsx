import type { Register, ThemeSetArgs } from 'claude-code'

import { makeColors } from './make-colors.js'
import { SCENE } from './scene.js'

// Night Fleet: deep-space blacks with a crimson fleet accent. A space scene only
// makes sense dark, so the look is dark-only.
const { theme, problems } = makeColors({
  label: 'Night Fleet',
  only: 'dark',
  // fleet crimson, hot orange, scanner green, warning amber, nebula violet
  roles: { accent: '#d23a46', danger: '#ff6a3d', success: '#4cb87e', warning: '#e3a63a', pro: '#8e7cff' },
  dark: {
    gray: {
      anchors: {
        'surface-0': '#06080c',
        'surface-1': '#0b0e14',
        'surface-2': '#0f131a',
        'surface-3': '#131821',
        'text-primary': '#e9edf3',
        'text-secondary': '#b6bec9',
        'text-muted': '#8f99a7',
      },
    },
  },
})

const LOOK: ThemeSetArgs = {
  colors: theme,
  // Thin frosting so the battle shows through while the words stay readable.
  backdrop: { scene: 'nightfleet', glass: { blur: 3, opacity: 0.25 } },
}

export const register: Register = on => {
  on('ui.render', { component: 'Backdrop' }, ($, e, next) => {
    if ((e.surface !== 'desktop' && e.surface !== 'mobile') || e.props.scene !== 'nightfleet') {
      return next(e)
    }
    const { Svg } = $.ui.resolve(e)

    return <Svg source={SCENE} alt="A hooded dark lord with a red blade watches a space battle" isInteractive />
  })

  on('session.start', async ($, e, next) => {
    const unpainted = problems.find(line => line.startsWith("Desktop won't paint"))

    if (unpainted !== undefined) {
      $.ui.toast(unpainted)
    }
    const set = await $.theme.set(LOOK)

    if (!set.isDrawn) {
      // A resumed session can start before the app reconnects. Check again for
      // a couple of minutes and clear the note once the app is drawing.
      $.ui.status(set.reason)
      let tries = 0
      const retry = $.clock.every(5000, () => {
        tries += 1
        void $.theme.set(LOOK).then(again => {
          if (again.isDrawn || tries >= 24) {
            retry.cancel()
            $.ui.status(again.isDrawn ? undefined : again.reason)
          }
        })
      })
    }

    return next(e)
  })
}
