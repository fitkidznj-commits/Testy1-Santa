import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
  Easing,
} from 'remotion';

const LAVENDER = '#c9b8f0';
const SOFT_PINK = '#f7c6e0';
const GOLD = '#f5d76e';
const WHITE = '#ffffff';
const DEEP_PURPLE = '#6a3fa0';

function Sparkle({ x, y, delay, size = 20 }) {
  const frame = useCurrentFrame();
  const t = (frame - delay) / 15;
  const opacity = interpolate(t, [0, 0.3, 0.7, 1], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const scale = interpolate(t, [0, 0.3, 1], [0.2, 1.2, 0.6], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const rotate = interpolate(t, [0, 1], [0, 90], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        opacity,
        transform: `scale(${scale}) rotate(${rotate}deg)`,
        fontSize: size,
        userSelect: 'none',
      }}
    >
      ✦
    </div>
  );
}

function FloatingParticle({ x, startY, speed, emoji, size }) {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const progress = ((frame * speed) % durationInFrames) / durationInFrames;
  const y = startY - progress * 700;
  const opacity = interpolate(y, [startY - 600, startY - 50, startY], [0, 0.8, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const sway = Math.sin(frame * 0.05 + x) * 15;

  return (
    <div
      style={{
        position: 'absolute',
        left: x + sway,
        top: y,
        opacity,
        fontSize: size,
        userSelect: 'none',
      }}
    >
      {emoji}
    </div>
  );
}

function TitleScene() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleScale = spring({ frame, fps, config: { damping: 12, stiffness: 80 } });
  const subtitleOpacity = interpolate(frame, [30, 55], [0, 1], { extrapolateRight: 'clamp' });
  const subtitleY = interpolate(frame, [30, 55], [20, 0], { extrapolateRight: 'clamp' });
  const bgOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  const sparkles = [
    { x: '8%', y: '15%', delay: 5, size: 28 },
    { x: '85%', y: '10%', delay: 12, size: 22 },
    { x: '5%', y: '75%', delay: 20, size: 18 },
    { x: '90%', y: '70%', delay: 8, size: 24 },
    { x: '50%', y: '8%', delay: 15, size: 20 },
    { x: '20%', y: '88%', delay: 25, size: 16 },
    { x: '75%', y: '85%', delay: 18, size: 22 },
    { x: '40%', y: '5%', delay: 3, size: 18 },
    { x: '60%', y: '92%', delay: 22, size: 20 },
  ];

  const particles = [
    { x: 80, startY: 800, speed: 0.4, emoji: '✨', size: 20 },
    { x: 200, startY: 850, speed: 0.3, emoji: '⭐', size: 16 },
    { x: 350, startY: 780, speed: 0.5, emoji: '✨', size: 14 },
    { x: 500, startY: 900, speed: 0.35, emoji: '💫', size: 18 },
    { x: 650, startY: 820, speed: 0.45, emoji: '✨', size: 22 },
    { x: 800, startY: 870, speed: 0.38, emoji: '⭐', size: 14 },
    { x: 950, startY: 800, speed: 0.42, emoji: '💫', size: 16 },
    { x: 1100, startY: 860, speed: 0.32, emoji: '✨', size: 20 },
  ];

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 40%, ${SOFT_PINK} 0%, ${LAVENDER} 50%, ${DEEP_PURPLE} 100%)`,
        opacity: bgOpacity,
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
      }}
    >
      {sparkles.map((s, i) => (
        <Sparkle key={i} {...s} />
      ))}
      {particles.map((p, i) => (
        <FloatingParticle key={i} {...p} />
      ))}

      <div style={{ textAlign: 'center', zIndex: 10 }}>
        <div
          style={{
            fontSize: 90,
            marginBottom: 10,
            transform: `scale(${titleScale})`,
            display: 'inline-block',
          }}
        >
          🧚
        </div>
        <div
          style={{
            fontFamily: 'Georgia, serif',
            fontSize: 96,
            fontWeight: 'bold',
            color: WHITE,
            textShadow: `0 0 30px ${GOLD}, 0 4px 12px rgba(0,0,0,0.3)`,
            transform: `scale(${titleScale})`,
            letterSpacing: '2px',
          }}
        >
          The Maid Fairy
        </div>
        <div
          style={{
            fontFamily: 'Georgia, serif',
            fontSize: 34,
            color: GOLD,
            marginTop: 18,
            opacity: subtitleOpacity,
            transform: `translateY(${subtitleY}px)`,
            textShadow: '0 2px 8px rgba(0,0,0,0.2)',
            letterSpacing: '1px',
          }}
        >
          ✦ Where every clean home is pure magic ✦
        </div>
      </div>
    </AbsoluteFill>
  );
}

function ServiceBubble({ emoji, label, delay }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const appear = spring({ frame: frame - delay, fps, config: { damping: 14, stiffness: 100 } });
  const opacity = interpolate(frame - delay, [0, 10], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 12,
        opacity,
        transform: `scale(${appear})`,
      }}
    >
      <div
        style={{
          width: 120,
          height: 120,
          borderRadius: '50%',
          background: `radial-gradient(circle at 35% 35%, ${WHITE}, ${LAVENDER})`,
          boxShadow: `0 8px 32px rgba(106,63,160,0.3), 0 0 0 3px ${GOLD}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 52,
        }}
      >
        {emoji}
      </div>
      <div
        style={{
          fontFamily: 'Georgia, serif',
          fontSize: 22,
          color: DEEP_PURPLE,
          fontWeight: 'bold',
          textAlign: 'center',
        }}
      >
        {label}
      </div>
    </div>
  );
}

function ServicesScene() {
  const frame = useCurrentFrame();
  const headingOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const headingY = interpolate(frame, [0, 20], [-30, 0], { extrapolateRight: 'clamp' });

  const services = [
    { emoji: '🏠', label: 'Deep Cleaning', delay: 10 },
    { emoji: '🫧', label: 'Sparkling Fresh', delay: 22 },
    { emoji: '🌸', label: 'Eco-Friendly', delay: 34 },
    { emoji: '⚡', label: 'Same-Day Magic', delay: 46 },
  ];

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(135deg, #f8f0ff 0%, #fce8f5 50%, #fff8e7 100%)`,
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        gap: 50,
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          fontFamily: 'Georgia, serif',
          fontSize: 56,
          fontWeight: 'bold',
          color: DEEP_PURPLE,
          textShadow: `0 2px 12px rgba(106,63,160,0.15)`,
          opacity: headingOpacity,
          transform: `translateY(${headingY}px)`,
        }}
      >
        ✦ Our Magical Services ✦
      </div>
      <div style={{ display: 'flex', gap: 60, alignItems: 'center' }}>
        {services.map((s, i) => (
          <ServiceBubble key={i} {...s} />
        ))}
      </div>
    </AbsoluteFill>
  );
}

function TestimonialScene() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cardScale = spring({ frame, fps, config: { damping: 14, stiffness: 80 } });
  const starsOpacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const textOpacity = interpolate(frame, [30, 55], [0, 1], { extrapolateRight: 'clamp' });
  const textY = interpolate(frame, [30, 55], [20, 0], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 60%, ${LAVENDER} 0%, ${DEEP_PURPLE} 100%)`,
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
      }}
    >
      {[...Array(12)].map((_, i) => (
        <FloatingParticle
          key={i}
          x={80 + i * 100}
          startY={900}
          speed={0.25 + i * 0.03}
          emoji={i % 2 === 0 ? '✨' : '⭐'}
          size={12 + (i % 3) * 4}
        />
      ))}

      <div
        style={{
          background: 'rgba(255,255,255,0.15)',
          backdropFilter: 'blur(12px)',
          borderRadius: 32,
          padding: '50px 70px',
          maxWidth: 800,
          textAlign: 'center',
          boxShadow: `0 20px 60px rgba(0,0,0,0.25), 0 0 0 2px rgba(255,255,255,0.3)`,
          transform: `scale(${cardScale})`,
        }}
      >
        <div style={{ fontSize: 42, opacity: starsOpacity, marginBottom: 20 }}>
          ⭐⭐⭐⭐⭐
        </div>
        <div
          style={{
            fontFamily: 'Georgia, serif',
            fontSize: 30,
            color: WHITE,
            lineHeight: 1.6,
            fontStyle: 'italic',
            opacity: textOpacity,
            transform: `translateY(${textY}px)`,
          }}
        >
          "My home has never looked — or felt — so magical.
          The Maid Fairy truly works wonders!"
        </div>
        <div
          style={{
            fontFamily: 'Georgia, serif',
            fontSize: 22,
            color: GOLD,
            marginTop: 24,
            opacity: textOpacity,
            transform: `translateY(${textY}px)`,
          }}
        >
          — Sarah M., Happy Customer
        </div>
      </div>
    </AbsoluteFill>
  );
}

function CtaScene() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoScale = spring({ frame, fps, config: { damping: 10, stiffness: 70 } });
  const ctaOpacity = interpolate(frame, [25, 50], [0, 1], { extrapolateRight: 'clamp' });
  const ctaScale = spring({ frame: frame - 25, fps, config: { damping: 12, stiffness: 90 } });
  const pulse = 1 + Math.sin(frame * 0.18) * 0.03;

  const sparkles = [
    { x: '12%', y: '20%', delay: 5, size: 26 },
    { x: '80%', y: '15%', delay: 15, size: 20 },
    { x: '6%', y: '70%', delay: 25, size: 18 },
    { x: '88%', y: '72%', delay: 10, size: 24 },
    { x: '45%', y: '6%', delay: 20, size: 22 },
    { x: '30%', y: '90%', delay: 8, size: 16 },
    { x: '70%', y: '88%', delay: 18, size: 20 },
  ];

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 30%, #fff8e7 0%, ${SOFT_PINK} 40%, ${LAVENDER} 80%, ${DEEP_PURPLE} 100%)`,
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        gap: 30,
        overflow: 'hidden',
      }}
    >
      {sparkles.map((s, i) => (
        <Sparkle key={i} {...s} />
      ))}

      <div
        style={{
          fontSize: 110,
          transform: `scale(${logoScale * pulse})`,
          filter: 'drop-shadow(0 8px 24px rgba(106,63,160,0.4))',
        }}
      >
        🧚‍♀️
      </div>
      <div
        style={{
          fontFamily: 'Georgia, serif',
          fontSize: 72,
          fontWeight: 'bold',
          color: DEEP_PURPLE,
          textShadow: `0 2px 16px rgba(106,63,160,0.2)`,
          transform: `scale(${logoScale})`,
          letterSpacing: '2px',
        }}
      >
        The Maid Fairy
      </div>
      <div
        style={{
          opacity: ctaOpacity,
          transform: `scale(${ctaScale})`,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 16,
        }}
      >
        <div
          style={{
            background: `linear-gradient(135deg, ${DEEP_PURPLE}, #9b59b6)`,
            color: WHITE,
            fontFamily: 'Georgia, serif',
            fontSize: 36,
            fontWeight: 'bold',
            padding: '20px 60px',
            borderRadius: 60,
            boxShadow: `0 10px 40px rgba(106,63,160,0.5)`,
            letterSpacing: '1px',
          }}
        >
          Book Your Magic Clean Today ✨
        </div>
        <div
          style={{
            fontFamily: 'Georgia, serif',
            fontSize: 26,
            color: DEEP_PURPLE,
            opacity: 0.8,
          }}
        >
          themaidfairy.com
        </div>
      </div>
    </AbsoluteFill>
  );
}

export function MaidFairy() {
  return (
    <AbsoluteFill style={{ background: '#000' }}>
      <Sequence from={0} durationInFrames={90}>
        <TitleScene />
      </Sequence>
      <Sequence from={90} durationInFrames={90}>
        <ServicesScene />
      </Sequence>
      <Sequence from={180} durationInFrames={90}>
        <TestimonialScene />
      </Sequence>
      <Sequence from={270} durationInFrames={90}>
        <CtaScene />
      </Sequence>
    </AbsoluteFill>
  );
}
