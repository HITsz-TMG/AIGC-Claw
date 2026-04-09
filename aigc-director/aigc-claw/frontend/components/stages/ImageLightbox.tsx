'use client';

import React, { useCallback, useEffect, useState } from 'react';
import { X, ChevronLeft, ChevronRight, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';
import { assetUrl } from './utils';

interface ImageLightboxProps {
  images: string[];        // 所有可浏览的图片路径
  initialIndex: number;    // 初始展示的索引
  onClose: () => void;
}

export default function ImageLightbox({ images, initialIndex, onClose }: ImageLightboxProps) {
  const [index, setIndex] = useState(initialIndex);
  const [scale, setScale] = useState(1);
  const [translate, setTranslate] = useState({ x: 0, y: 0 });
  const [dragging, setDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  const current = images[index];
  const hasPrev = index > 0;
  const hasNext = index < images.length - 1;

  const resetView = useCallback(() => {
    setScale(1);
    setTranslate({ x: 0, y: 0 });
  }, []);

  const goPrev = useCallback(() => {
    if (hasPrev) { setIndex(i => i - 1); resetView(); }
  }, [hasPrev, resetView]);

  const goNext = useCallback(() => {
    if (hasNext) { setIndex(i => i + 1); resetView(); }
  }, [hasNext, resetView]);

  const zoomIn = useCallback(() => setScale(s => Math.min(s * 1.5, 5)), []);
  const zoomOut = useCallback(() => {
    setScale(s => {
      const next = Math.max(s / 1.5, 1);
      if (next === 1) setTranslate({ x: 0, y: 0 });
      return next;
    });
  }, []);

  // 键盘导航
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      switch (e.key) {
        case 'Escape': onClose(); break;
        case 'ArrowLeft': goPrev(); break;
        case 'ArrowRight': goNext(); break;
        case '+': case '=': zoomIn(); break;
        case '-': zoomOut(); break;
        case '0': resetView(); break;
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onClose, goPrev, goNext, zoomIn, zoomOut, resetView]);

  // 滚轮缩放
  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault();
    if (e.deltaY < 0) {
      setScale(s => Math.min(s * 1.15, 5));
    } else {
      setScale(s => {
        const next = Math.max(s / 1.15, 1);
        if (next === 1) setTranslate({ x: 0, y: 0 });
        return next;
      });
    }
  }, []);

  // 拖拽平移（缩放 > 1 时）
  const handlePointerDown = useCallback((e: React.PointerEvent) => {
    if (scale <= 1) return;
    setDragging(true);
    setDragStart({ x: e.clientX - translate.x, y: e.clientY - translate.y });
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
  }, [scale, translate]);

  const handlePointerMove = useCallback((e: React.PointerEvent) => {
    if (!dragging) return;
    setTranslate({ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y });
  }, [dragging, dragStart]);

  const handlePointerUp = useCallback(() => setDragging(false), []);

  // 禁止背景滚动
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = ''; };
  }, []);

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center">
      {/* 遮罩 */}
      <div
        className="absolute inset-0 bg-black/80 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* 顶部工具栏 */}
      <div className="absolute top-0 left-0 right-0 z-10 flex items-center justify-between px-4 py-3">
        <div className="text-white/70 text-sm font-medium">
          {images.length > 1 && `${index + 1} / ${images.length}`}
        </div>
        <div className="flex items-center gap-1">
          <button onClick={zoomOut} className="w-8 h-8 rounded-full flex items-center justify-center text-white/70 hover:text-white hover:bg-white/10 transition-colors" title="缩小 (-)">
            <ZoomOut className="w-4 h-4" />
          </button>
          <span className="text-white/50 text-xs w-12 text-center">{Math.round(scale * 100)}%</span>
          <button onClick={zoomIn} className="w-8 h-8 rounded-full flex items-center justify-center text-white/70 hover:text-white hover:bg-white/10 transition-colors" title="放大 (+)">
            <ZoomIn className="w-4 h-4" />
          </button>
          <button onClick={resetView} className="w-8 h-8 rounded-full flex items-center justify-center text-white/70 hover:text-white hover:bg-white/10 transition-colors" title="重置 (0)">
            <RotateCcw className="w-4 h-4" />
          </button>
          <div className="w-px h-5 bg-white/20 mx-1" />
          <button onClick={onClose} className="w-8 h-8 rounded-full flex items-center justify-center text-white/70 hover:text-white hover:bg-white/10 transition-colors" title="关闭 (Esc)">
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* 左右切换 */}
      {hasPrev && (
        <button
          onClick={goPrev}
          aria-label="上一张 (左方向键)"
          title="上一张 (左方向键)"
          className="absolute left-4 top-1/2 -translate-y-1/2 z-10 w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors"
        >
          <ChevronLeft className="w-6 h-6" />
        </button>
      )}
      {hasNext && (
        <button
          onClick={goNext}
          aria-label="下一张 (右方向键)"
          title="下一张 (右方向键)"
          className="absolute right-4 top-1/2 -translate-y-1/2 z-10 w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors"
        >
          <ChevronRight className="w-6 h-6" />
        </button>
      )}

      {/* 图片 */}
      <div
        className="relative z-[1] max-w-[90vw] max-h-[85vh] select-none"
        onWheel={handleWheel}
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
        style={{ cursor: scale > 1 ? (dragging ? 'grabbing' : 'grab') : 'zoom-in' }}
      >
        <img
          src={assetUrl(current)}
          alt={`image ${index + 1}`}
          className="max-w-[90vw] max-h-[85vh] object-contain rounded-lg shadow-2xl"
          style={{
            transform: `scale(${scale}) translate(${translate.x / scale}px, ${translate.y / scale}px)`,
            transition: dragging ? 'none' : 'transform 0.2s ease',
          }}
          draggable={false}
          onClick={(e) => {
            if (scale === 1) {
              e.stopPropagation();
              zoomIn();
            }
          }}
        />
      </div>

      {/* 底部缩略图条 */}
      {images.length > 1 && (
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-10 flex gap-2 bg-black/40 rounded-full px-3 py-2">
          {images.map((path, i) => (
            <button
              key={path}
              onClick={() => { setIndex(i); resetView(); }}
              className={`w-10 h-10 rounded overflow-hidden border-2 transition-all ${
                i === index ? 'border-white shadow-lg scale-110' : 'border-transparent opacity-60 hover:opacity-100'
              }`}
            >
              <img src={assetUrl(path)} alt={`thumb ${i + 1}`} className="w-full h-full object-cover" />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
