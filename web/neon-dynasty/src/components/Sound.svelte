<script lang="ts" module>
	import { sound, type MusicName, type SoundEffectName, type SoundName } from '../game/sound';

	export type EmitterEventSound =
		| { type: 'soundMusic'; name: MusicName }
		| { type: 'soundOnce'; name: SoundEffectName; forcePlay?: boolean }
		| { type: 'soundLoop'; name: SoundEffectName }
		| { type: 'soundStop'; name: SoundName }
		| { type: 'soundFade'; name: SoundName; from: number; to: number; duration: number }
		| { type: 'soundScatterCounterIncrease' }
		| { type: 'soundScatterCounterClear' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';

	import { waitForTimeout } from 'utils-shared/wait';
	import { SECOND } from 'constants-shared/time';
	import { stateBet } from 'state-shared';

	import { getContext } from '../game/context';

	const context = getContext();

	context.eventEmitter.subscribeOnMount({
		// ui
		soundBetMode: async ({ betModeKey }) => {
			if (betModeKey === 'super') {
				// check if super, when changing the bet mode.
				sound.players.once.play({ name: 'nd_sfx_winlevel_end' });
				await waitForTimeout(SECOND);
				sound.players.music.play({ name: 'nd_bgm_freespin' });
			} else {
				sound.players.music.play({ name: 'nd_bgm_main' });
			}
		},
		soundPressGeneral: () => sound.players.once.play({ name: 'nd_sfx_btn_general' }),
		soundPressBet: () => sound.players.once.play({ name: 'nd_sfx_btn_spin' }),
		// scatterCounter
		soundScatterCounterIncrease: () => (context.stateGame.scatterCounter = context.stateGame.scatterCounter + 1), // prettier-ignore
		soundScatterCounterClear: () => (context.stateGame.scatterCounter = 0),
		// game
		soundMusic: ({ name }) => sound.players.music.play({ name }),
		soundLoop: ({ name }) => sound.players.loop.play({ name }),
		soundOnce: ({ name, forcePlay }) => sound.players.once.play({ name, forcePlay }),
		soundStop: ({ name }) => sound.stop({ name }),
		soundFade: async ({ name, duration, from, to }) => await sound.fade({ name, duration, from, to }), // prettier-ignore
		soundMute: ({ muted }) => (muted ? sound.disable() : sound.enable()),
		musicMute: ({ muted }) => sound.players.music.volume(muted ? 0 : 1),
	});

	onMount(() => {
		if (stateBet.activeBetModeKey === 'super') {
			// check if super, when resume bet and the bet is a super spin.
			sound.players.music.play({ name: 'nd_bgm_freespin' });
		} else {
			sound.players.music.play({ name: 'nd_bgm_main' });

			//How to control volume per soundfile(use fade)
			// sound.players.music.fade({ name: 'nd_bgm_main', from: 0, to: 1, duration: 3000 });

			//How to control rate per soundfile
			// sound.players.music.rate({ rate: 2, name: 'nd_bgm_main'}); // change play back rate(1: default, 0: slow, 1+ fasterm and higher pitch )
		}
	});
</script>
